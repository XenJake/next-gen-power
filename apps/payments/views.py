from decimal import Decimal, InvalidOperation
import logging

from django.conf import settings
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.charging.models import ChargingSession, Charger

from .models import Payment
from .providers import get_payment_provider

logger = logging.getLogger(__name__)


def authorize_paid_session(session_id):
	from apps.charging.controllers import get_charger_controller

	controller = get_charger_controller()
	if not controller:
		return False

	session = ChargingSession.objects.select_related('charger').get(pk=session_id)
	if session.status != ChargingSession.Status.PAID_PENDING_AUTH:
		return session.status == ChargingSession.Status.AUTHORIZED

	try:
		authorized = controller.authorize(session)
	except Exception:
		logger.exception('Charger authorization failed for session %s', session.public_id)
		return False
	if not authorized:
		return False

	with transaction.atomic():
		locked_session = ChargingSession.objects.select_for_update().get(pk=session_id)
		if locked_session.status != ChargingSession.Status.PAID_PENDING_AUTH:
			return locked_session.status == ChargingSession.Status.AUTHORIZED
		Charger.objects.select_for_update().get(pk=locked_session.charger_id)
		locked_session.status = ChargingSession.Status.AUTHORIZED
		locked_session.started_at = timezone.now()
		locked_session.save(update_fields=['status', 'started_at', 'updated_at'])
		Charger.objects.filter(pk=locked_session.charger_id).update(status=Charger.Status.IN_USE)
	return True


def checkout(request, public_id):
	payment = get_object_or_404(Payment.objects.select_related('session__charger__station'), public_id=public_id)
	if payment.status != Payment.Status.PENDING:
		return render(request, 'payments/result.html', {'payment': payment})
	provider = get_payment_provider()
	if not provider:
		return render(request, 'payments/checkout.html', {'payment': payment, 'provider_ready': False}, status=503)
	if request.method == 'POST':
		checkout_url = provider.create_checkout(payment, request)
		return redirect(checkout_url)
	return render(request, 'payments/checkout.html', {'payment': payment, 'provider_ready': True})


@csrf_exempt
@require_POST
def webhook(request):
	provider = get_payment_provider()
	if not provider:
		return HttpResponse('Payment provider is not configured.', status=503)
	try:
		event = provider.verify_webhook(request)
	except Exception:
		return HttpResponseBadRequest('Webhook verification failed.')
	if not event or event.get('status') != 'succeeded':
		return HttpResponse('Event ignored.', status=200)
	try:
		payment_id = event['payment_id']
		amount = Decimal(str(event['amount']))
		currency = event['currency']
		reference = event['reference']
	except (KeyError, TypeError, InvalidOperation):
		return HttpResponseBadRequest('Invalid payment event.')

	with transaction.atomic():
		payment = get_object_or_404(Payment.objects.select_for_update().select_related('session'), public_id=payment_id)
		if payment.amount != amount or payment.currency != currency:
			return HttpResponseBadRequest('Payment amount or currency mismatch.')
		if payment.status == Payment.Status.PENDING:
			payment.status = Payment.Status.SUCCEEDED
			payment.provider = settings.PAYMENT_PROVIDER
			payment.provider_reference = reference
			payment.save(update_fields=['status', 'provider', 'provider_reference', 'updated_at'])
			ChargingSession.objects.filter(pk=payment.session_id, status=ChargingSession.Status.PENDING_PAYMENT).update(
				status=ChargingSession.Status.PAID_PENDING_AUTH,
				updated_at=timezone.now(),
			)
		elif payment.status != Payment.Status.SUCCEEDED:
			return HttpResponse('Payment is not pending.', status=200)
		session_id = payment.session_id

	if authorize_paid_session(session_id):
		return HttpResponse('Payment recorded and charger authorized.', status=200)
	return HttpResponse('Payment recorded; charger authorization is pending.', status=200)
