from datetime import timedelta
from decimal import Decimal

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.vehicles.models import Manufacturer, Vehicle

from .models import ChargerProduct, Payment, SeasonalDeal, VehicleOrder
from .pricing import active_seasonal_deal, build_order_quote, vehicle_price_in_ghs


class CommercePricingTests(TestCase):
	def setUp(self):
		self.manufacturer = Manufacturer.objects.create(name='Test Motors')
		self.vehicle = Vehicle.objects.create(
			manufacturer=self.manufacturer,
			model_name='Test EV',
			slug='test-ev',
			description='A test vehicle.',
			price=Decimal('40000.00'),
			currency='USD',
			is_published=True,
		)
		self.standard = ChargerProduct.objects.get(product_type=ChargerProduct.ProductType.STANDARD)
		self.premium = ChargerProduct.objects.get(product_type=ChargerProduct.ProductType.PREMIUM)

	@override_settings(USD_GHS_EXCHANGE_RATE=Decimal('11.70343'), BUNDLE_DISCOUNT_PERCENT=Decimal('5.00'))
	def test_usd_vehicle_is_converted_to_ghs_for_purchase(self):
		self.assertEqual(vehicle_price_in_ghs(self.vehicle), Decimal('468137.20'))

	@override_settings(USD_GHS_EXCHANGE_RATE=Decimal('11.70343'), BUNDLE_DISCOUNT_PERCENT=Decimal('5.00'))
	def test_bundle_discount_applies_to_vehicle_and_charger_total(self):
		quote = build_order_quote(vehicle=self.vehicle, charger_product=self.standard)
		self.assertEqual(quote['vehicle_amount'], Decimal('468137.20'))
		self.assertEqual(quote['charger_amount'], Decimal('3999.00'))
		self.assertEqual(quote['bundle_discount'], Decimal('23606.81'))
		self.assertEqual(quote['amount'], Decimal('448529.39'))

	def test_charger_only_quote_has_no_bundle_discount(self):
		quote = build_order_quote(charger_product=self.premium)
		self.assertEqual(quote['amount'], Decimal('4999.00'))
		self.assertEqual(quote['bundle_discount'], Decimal('0.00'))

	def test_active_seasonal_deal_is_selected_only_during_its_window(self):
		now = timezone.now()
		deal = SeasonalDeal.objects.create(
			name='Test season',
			discount_percent=Decimal('10.00'),
			starts_at=now - timedelta(days=1),
			ends_at=now + timedelta(days=1),
			is_active=True,
		)
		self.assertEqual(active_seasonal_deal(now), deal)
		deal.is_active = False
		deal.save(update_fields=['is_active', 'updated_at'])
		self.assertIsNone(active_seasonal_deal(now))

	@override_settings(USD_GHS_EXCHANGE_RATE=Decimal('11.70343'), BUNDLE_DISCOUNT_PERCENT=Decimal('5.00'))
	def test_seasonal_deal_and_bundle_discounts_are_snapshotted_separately(self):
		deal = SeasonalDeal.objects.create(
			name='Test season',
			discount_percent=Decimal('10.00'),
			starts_at=timezone.now() - timedelta(days=1),
			ends_at=timezone.now() + timedelta(days=1),
			is_active=True,
		)
		quote = build_order_quote(vehicle=self.vehicle, charger_product=self.standard, deal=deal)
		self.assertEqual(quote['seasonal_discount'], Decimal('46813.72'))
		self.assertEqual(quote['bundle_discount'], Decimal('21266.12'))
		self.assertEqual(quote['amount'], Decimal('404056.36'))


class CommerceOrderFlowTests(TestCase):
	def setUp(self):
		self.manufacturer = Manufacturer.objects.create(name='Test Motors')
		self.vehicle = Vehicle.objects.create(
			manufacturer=self.manufacturer,
			model_name='Test EV',
			slug='test-ev',
			description='A test vehicle.',
			price=Decimal('40000.00'),
			currency='USD',
			is_published=True,
		)
		self.standard = ChargerProduct.objects.get(product_type=ChargerProduct.ProductType.STANDARD)
		self.premium = ChargerProduct.objects.get(product_type=ChargerProduct.ProductType.PREMIUM)
		self.customer = {
			'customer_name': 'Ama Test',
			'customer_email': 'ama@example.com',
			'customer_phone': '0240000000',
		}

	def test_vehicle_and_charger_pages_show_purchase_options(self):
		response = self.client.get(self.vehicle.get_absolute_url())
		self.assertContains(response, 'Buy this vehicle')
		self.assertContains(response, 'GHS 468,137.20')
		response = self.client.get(reverse('payments:charger_store'))
		self.assertContains(response, 'GHS 3,999.00')
		self.assertContains(response, 'GHS 4,999.00')
		self.assertContains(response, 'installation is quoted separately')

	@override_settings(
		USD_GHS_EXCHANGE_RATE=Decimal('11.70343'),
		BUNDLE_DISCOUNT_PERCENT=Decimal('5.00'),
		PAYMENT_PROVIDER_CLASS='apps.payments.providers.MockPaymentProvider',
	)
	def test_customer_can_mock_buy_vehicle_and_charger(self):
		response = self.client.post(
			reverse('payments:start_vehicle_order', args=[self.vehicle.slug]),
			{**self.customer, 'charger_product': str(self.standard.pk)},
		)
		order = VehicleOrder.objects.get()
		self.assertRedirects(response, reverse('payments:order_checkout', args=[order.public_id]))
		self.assertEqual(order.amount, Decimal('448529.39'))

		response = self.client.post(
			reverse('payments:order_checkout', args=[order.public_id]),
			{'method': Payment.Method.MTN_MOMO},
		)
		self.assertRedirects(response, reverse('payments:mock_order_checkout', args=[order.public_id]))
		response = self.client.post(reverse('payments:mock_order_checkout', args=[order.public_id]))
		self.assertRedirects(response, reverse('payments:order_checkout', args=[order.public_id]))

		order.refresh_from_db()
		self.assertEqual(order.status, VehicleOrder.Status.MOCK_PAID)
		self.assertTrue(order.mock_reference.startswith('MOCK-'))
		self.assertIsNotNone(order.paid_at)
		self.assertEqual(Payment.objects.count(), 0)
		self.assertContains(
			self.client.get(reverse('payments:order_checkout', args=[order.public_id])),
			'No real payment was taken',
		)

	@override_settings(PAYMENT_PROVIDER_CLASS='apps.payments.providers.MockPaymentProvider')
	def test_customer_can_mock_buy_home_charger_without_vehicle(self):
		response = self.client.post(reverse('payments:charger_store'), {
			**self.customer,
			'charger_product': str(self.premium.pk),
		})
		order = VehicleOrder.objects.get()
		self.assertRedirects(response, reverse('payments:order_checkout', args=[order.public_id]))
		self.assertIsNone(order.vehicle)
		self.assertEqual(order.charger_product, self.premium)
		self.assertEqual(order.amount, Decimal('4999.00'))

	@override_settings(PAYMENT_PROVIDER_CLASS='')
	def test_order_checkout_is_unavailable_without_mock_provider(self):
		order = VehicleOrder.objects.create(
			vehicle=self.vehicle,
			vehicle_name=str(self.vehicle),
			customer_name='Ama Test',
			customer_email='ama@example.com',
			customer_phone='0240000000',
			vehicle_amount=Decimal('468137.20'),
			amount=Decimal('468137.20'),
		)
		response = self.client.get(reverse('payments:order_checkout', args=[order.public_id]))
		self.assertEqual(response.status_code, 503)
		order.refresh_from_db()
		self.assertEqual(order.status, VehicleOrder.Status.PENDING)

	def test_vehicle_order_form_rejects_missing_contact_details(self):
		response = self.client.post(
			reverse('payments:start_vehicle_order', args=[self.vehicle.slug]),
			{'customer_email': 'not-an-email'},
		)
		self.assertEqual(response.status_code, 400)
		self.assertContains(response, 'This field is required', status_code=400)
		self.assertFalse(VehicleOrder.objects.exists())

	@override_settings(PAYMENT_PROVIDER_CLASS='apps.payments.providers.MockPaymentProvider')
	def test_sold_vehicle_cannot_be_ordered(self):
		self.vehicle.availability = Vehicle.Availability.SOLD
		self.vehicle.save(update_fields=['availability', 'updated_at'])
		response = self.client.post(
			reverse('payments:start_vehicle_order', args=[self.vehicle.slug]),
			self.customer,
		)
		self.assertEqual(response.status_code, 400)
		self.assertContains(response, 'marked sold', status_code=400)
		self.assertFalse(VehicleOrder.objects.exists())

	@override_settings(PAYMENT_PROVIDER_CLASS='apps.payments.providers.MockPaymentProvider')
	def test_invalid_payment_method_does_not_mark_order_paid(self):
		order = VehicleOrder.objects.create(
			vehicle=self.vehicle,
			vehicle_name=str(self.vehicle),
			customer_name='Ama Test',
			customer_email='ama@example.com',
			customer_phone='0240000000',
			vehicle_amount=Decimal('468137.20'),
			amount=Decimal('468137.20'),
			method='crypto',
		)
		response = self.client.post(reverse('payments:mock_order_checkout', args=[order.public_id]))
		self.assertRedirects(response, reverse('payments:order_checkout', args=[order.public_id]))
		order.refresh_from_db()
		self.assertEqual(order.status, VehicleOrder.Status.PENDING)
		self.assertEqual(order.mock_reference, '')
