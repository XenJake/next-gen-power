from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.vehicles.models import Vehicle
from apps.vehicles.forms import VehicleEnquiryForm

from .forms import (
	ChargerPurchaseForm,
	CheckoutMethodForm,
	PAYMENT_METHOD_CHOICES,
	VehiclePurchaseForm,
)
from .models import ChargerProduct, VehicleOrder
from .pricing import active_seasonal_deal, build_order_quote, published_chargers, vehicle_price_in_ghs
from .providers import MockPaymentProvider, get_payment_provider


def charger_store(request):
	form = ChargerPurchaseForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		product = form.cleaned_data['charger_product']
		quote = build_order_quote(charger_product=product)
		order = VehicleOrder.objects.create(
			charger_product=product,
			charger_name=product.name,
			customer_name=form.cleaned_data['customer_name'],
			customer_email=form.cleaned_data['customer_email'],
			customer_phone=form.cleaned_data['customer_phone'],
			**quote,
		)
		return redirect('payments:order_checkout', public_id=order.public_id)
	return render(request, 'payments/charger_store.html', {
		'form': form,
		'chargers': published_chargers(),
	})


@require_POST
def start_vehicle_order(request, slug):
	vehicle = get_object_or_404(
		Vehicle.objects.select_related('manufacturer').prefetch_related('images'),
		slug=slug,
		is_published=True,
	)
	form = VehiclePurchaseForm(request.POST)
	form_is_valid = form.is_valid()
	deal = active_seasonal_deal()
	if vehicle.availability == Vehicle.Availability.SOLD:
		form.add_error(None, 'This vehicle is marked sold and cannot be ordered.')
	elif vehicle_price_in_ghs(vehicle) is None:
		form.add_error(None, 'A confirmed GHS purchase price is not available for this vehicle.')
	elif form_is_valid:
		product = form.cleaned_data['charger_product']
		quote = build_order_quote(vehicle=vehicle, charger_product=product, deal=deal)
		order = VehicleOrder.objects.create(
			vehicle=vehicle,
			charger_product=product,
			vehicle_name=str(vehicle),
			charger_name=product.name if product else '',
			customer_name=form.cleaned_data['customer_name'],
			customer_email=form.cleaned_data['customer_email'],
			customer_phone=form.cleaned_data['customer_phone'],
			**quote,
		)
		return redirect('payments:order_checkout', public_id=order.public_id)
	quote = build_order_quote(vehicle=vehicle, deal=deal) if vehicle_price_in_ghs(vehicle) is not None else None
	return render(request, 'vehicles/detail.html', {
		'vehicle': vehicle,
		'form': VehicleEnquiryForm(),
		'purchase_form': form,
		'quote': quote,
		'active_deal': deal,
		'exchange_rate': settings.USD_GHS_EXCHANGE_RATE,
		'rate_as_of': settings.USD_GHS_RATE_AS_OF,
	}, status=400)


def order_checkout(request, public_id):
	order = get_object_or_404(
		VehicleOrder.objects.select_related('vehicle', 'charger_product'),
		public_id=public_id,
	)
	if order.status != VehicleOrder.Status.PENDING:
		return render(request, 'payments/order_result.html', {'order': order})
	provider = get_payment_provider()
	if not isinstance(provider, MockPaymentProvider):
		return render(request, 'payments/order_checkout.html', {
			'order': order,
			'provider_ready': False,
			'form': CheckoutMethodForm(),
		}, status=503)
	form = CheckoutMethodForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		with transaction.atomic():
			locked_order = VehicleOrder.objects.select_for_update().get(pk=order.pk)
			if locked_order.status != VehicleOrder.Status.PENDING:
				return redirect('payments:order_checkout', public_id=locked_order.public_id)
			locked_order.method = form.cleaned_data['method']
			locked_order.save(update_fields=['method', 'updated_at'])
		return redirect('payments:mock_order_checkout', public_id=order.public_id)
	return render(request, 'payments/order_checkout.html', {
		'order': order,
		'provider_ready': True,
		'form': form,
	})


def mock_order_checkout(request, public_id):
	provider = get_payment_provider()
	if not isinstance(provider, MockPaymentProvider):
		return HttpResponse('Mock checkout is not enabled.', status=404)
	order = get_object_or_404(VehicleOrder, public_id=public_id)
	if order.status != VehicleOrder.Status.PENDING:
		return redirect('payments:order_checkout', public_id=order.public_id)
	if order.method not in dict(PAYMENT_METHOD_CHOICES):
		return redirect('payments:order_checkout', public_id=order.public_id)
	if request.method == 'POST':
		with transaction.atomic():
			order = VehicleOrder.objects.select_for_update().get(pk=order.pk)
			if order.status == VehicleOrder.Status.PENDING:
				order.status = VehicleOrder.Status.MOCK_PAID
				order.mock_reference = provider.create_mock_reference()
				order.paid_at = timezone.now()
				order.save(update_fields=['status', 'mock_reference', 'paid_at', 'updated_at'])
		return redirect('payments:order_checkout', public_id=order.public_id)
	return render(request, 'payments/order_mock_checkout.html', {'order': order})
