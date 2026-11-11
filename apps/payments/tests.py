import json

from django.test import TestCase, override_settings
from django.urls import reverse

from apps.charging.models import Charger, ChargingSession, ChargingStation

from .models import Payment


class TestPaymentProvider:
	def verify_webhook(self, request):
		return json.loads(request.body)


class TestChargerController:
	def authorize(self, session):
		return True


class PaymentSafetyTests(TestCase):
	def setUp(self):
		station = ChargingStation.objects.create(name='Test', slug='test', address='Test Road', city='Accra', is_published=True)
		charger = Charger.objects.create(station=station, charger_code='A1', connector_type='CCS2', max_power_kw=60)
		session = ChargingSession.objects.create(charger=charger, amount='20.00')
		self.payment = Payment.objects.create(session=session, method=Payment.Method.CARD, amount='20.00')

	@override_settings(PAYMENT_PROVIDER_CLASS='')
	def test_checkout_is_unavailable_without_provider(self):
		response = self.client.get(reverse('payments:checkout', args=[self.payment.public_id]))
		self.assertEqual(response.status_code, 503)
		self.assertEqual(Payment.objects.get(pk=self.payment.pk).status, Payment.Status.PENDING)

	@override_settings(PAYMENT_PROVIDER_CLASS='')
	def test_webhook_cannot_mark_payment_paid_without_provider(self):
		response = self.client.post(reverse('payments:webhook'), data='{}', content_type='application/json')
		self.assertEqual(response.status_code, 503)
		self.assertEqual(Payment.objects.get(pk=self.payment.pk).status, Payment.Status.PENDING)

	def payment_event(self):
		return json.dumps({
			'payment_id': str(self.payment.public_id),
			'status': 'succeeded',
			'amount': '20.00',
			'currency': 'GHS',
			'reference': 'test-reference',
		})

	@override_settings(
		PAYMENT_PROVIDER_CLASS='apps.payments.tests.TestPaymentProvider',
		PAYMENT_PROVIDER='test',
		CHARGER_CONTROLLER_CLASS='',
	)
	def test_confirmed_payment_remains_visible_if_controller_is_unavailable(self):
		response = self.client.post(reverse('payments:webhook'), data=self.payment_event(), content_type='application/json')
		self.assertEqual(response.status_code, 200)
		self.payment.refresh_from_db()
		self.payment.session.refresh_from_db()
		self.assertEqual(self.payment.status, Payment.Status.SUCCEEDED)
		self.assertEqual(self.payment.session.status, ChargingSession.Status.PAID_PENDING_AUTH)

	@override_settings(
		PAYMENT_PROVIDER_CLASS='apps.payments.tests.TestPaymentProvider',
		PAYMENT_PROVIDER='test',
		CHARGER_CONTROLLER_CLASS='apps.payments.tests.TestChargerController',
	)
	def test_verified_payment_authorizes_charger_through_controller(self):
		response = self.client.post(reverse('payments:webhook'), data=self.payment_event(), content_type='application/json')
		self.assertEqual(response.status_code, 200)
		self.payment.refresh_from_db()
		self.payment.session.refresh_from_db()
		self.payment.session.charger.refresh_from_db()
		self.assertEqual(self.payment.status, Payment.Status.SUCCEEDED)
		self.assertEqual(self.payment.session.status, ChargingSession.Status.AUTHORIZED)
		self.assertEqual(self.payment.session.charger.status, Charger.Status.IN_USE)
