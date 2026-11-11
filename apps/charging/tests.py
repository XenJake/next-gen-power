from django.test import TestCase, override_settings
from django.urls import reverse

from apps.payments.models import Payment

from .models import Charger, ChargingSession, ChargingStation


class ChargingFlowTests(TestCase):
	def setUp(self):
		self.station = ChargingStation.objects.create(
			name='Test Station', slug='test-station', address='1 Test Road',
			city='Accra', latitude='5.603700', longitude='-0.187000', is_published=True,
		)
		self.charger = Charger.objects.create(
			station=self.station, charger_code='A1', connector_type='CCS2',
			max_power_kw=120, status=Charger.Status.AVAILABLE,
		)

	def test_station_and_qr_pages_render(self):
		self.assertEqual(self.client.get(reverse('charging:station_list')).status_code, 200)
		self.assertEqual(self.client.get(self.charger.get_qr_url()).status_code, 200)

	def test_published_charger_has_scannable_svg_qr(self):
		response = self.client.get(reverse('charging:charger_qr_svg', args=[self.charger.public_id]))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response['Content-Type'], 'image/svg+xml')
		self.assertIn(b'<svg', response.content)

	@override_settings(PAYMENT_PROVIDER_CLASS='apps.payments.tests.TestPaymentProvider')
	def test_qr_start_creates_pending_records_without_authorizing_charger(self):
		response = self.client.post(reverse('charging:start_session', args=[self.charger.public_id]), {
			'amount': '25.00', 'method': 'mobile_money',
		})
		session = ChargingSession.objects.get()
		payment = Payment.objects.get(session=session)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['Location'], reverse('payments:checkout', args=[payment.public_id]))
		self.assertEqual(session.status, ChargingSession.Status.PENDING_PAYMENT)
		self.assertEqual(payment.status, Payment.Status.PENDING)
		self.assertEqual(self.charger.status, Charger.Status.AVAILABLE)

	def test_qr_start_does_not_create_records_without_payment_provider(self):
		response = self.client.post(reverse('charging:start_session', args=[self.charger.public_id]), {
			'amount': '25.00', 'method': 'mobile_money',
		})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(ChargingSession.objects.count(), 0)
		self.assertEqual(Payment.objects.count(), 0)

	def test_station_status_api_reports_available_charger(self):
		response = self.client.get(reverse('charging:charger_api', args=[self.charger.public_id]))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()['status'], Charger.Status.AVAILABLE)

	def test_station_city_and_charger_status_filters(self):
		response = self.client.get(reverse('charging:station_list'), {'city': 'Accra', 'status': 'available'})
		self.assertContains(response, 'Test Station')
		self.assertContains(response, 'station-map-data')
		filtered_out = self.client.get(reverse('charging:station_list'), {'city': 'Accra', 'status': 'offline'})
		self.assertNotContains(filtered_out, 'Test Station')

	def test_charging_guide_explains_qr_and_payment(self):
		response = self.client.get(reverse('charging:how_it_works'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Scan the QR code')
		self.assertContains(response, 'mobile money')
