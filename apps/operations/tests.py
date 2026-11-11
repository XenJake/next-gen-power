from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from apps.charging.models import Charger, ChargingStation
from apps.operations.models import FaultReport, MaintenanceRecord
from apps.vehicles.models import Manufacturer, Vehicle


class OperationsAccessTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username='operator', is_staff=True,
		)

	def test_dashboard_requires_login(self):
		response = self.client.get(reverse('operations:dashboard'))
		self.assertEqual(response.status_code, 302)
		self.assertIn('/accounts/login/', response['Location'])

	def test_staff_without_permission_is_denied(self):
		self.client.force_login(self.user)
		self.assertEqual(self.client.get(reverse('operations:dashboard')).status_code, 403)

	def test_staff_with_session_permission_can_view_dashboard(self):
		permission_codenames = ['view_chargingstation', 'view_charger', 'view_chargingsession']
		permissions = Permission.objects.filter(
			content_type__app_label='charging',
			codename__in=permission_codenames,
		)
		self.user.user_permissions.add(*permissions)
		self.user.user_permissions.add(Permission.objects.get(
			codename='view_payment',
			content_type__app_label='payments',
		))
		self.client.force_login(self.user)
		response = self.client.get(reverse('operations:dashboard'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Network overview')
		self.assertNotContains(response, 'Open Django admin')


class CustomOperationsTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username='network-admin', is_staff=True, is_superuser=True,
		)
		self.client.force_login(self.user)
		self.manufacturer = Manufacturer.objects.create(name='BYD')
		self.station = ChargingStation.objects.create(
			name='Accra Operations Site', slug='accra-operations-site',
			site_type=ChargingStation.SiteType.MALL, address='Accra Mall', city='Accra',
		)

	def test_custom_navigation_lists_operations_areas(self):
		response = self.client.get(reverse('operations:dashboard'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Charger fleet')
		self.assertContains(response, 'Vehicle inventory')
		self.assertContains(response, 'Maintenance')

	def test_station_can_be_created_and_filtered(self):
		response = self.client.post(reverse('operations:station_create'), {
			'name': 'West Hills Site', 'slug': 'west-hills-site', 'site_type': 'mall',
			'address': 'New Weija', 'city': 'Accra', 'region': 'Greater Accra',
			'latitude': '', 'longitude': '', 'opening_hours': '', 'amenities': '',
			'status': 'operational', 'solar_capacity_kw': '', 'battery_storage_kwh': '',
			'is_demo': 'on', 'is_published': 'on',
		})
		self.assertRedirects(response, reverse('operations:stations'))
		self.assertTrue(ChargingStation.objects.filter(slug='west-hills-site', is_demo=True).exists())
		listing = self.client.get(reverse('operations:stations'), {'q': 'West Hills'})
		self.assertContains(listing, 'West Hills Site')

	def test_charger_can_be_created_with_ac_dc_specifications(self):
		response = self.client.post(reverse('operations:charger_create'), {
			'station': self.station.pk, 'charger_code': 'AC-01', 'power_type': 'ac',
			'connector_type': 'Type 2', 'max_power_kw': '22', 'status': 'available',
			'is_demo': 'on', 'external_reference': '',
		})
		self.assertRedirects(response, reverse('operations:chargers'))
		charger = Charger.objects.get(charger_code='AC-01')
		self.assertEqual(charger.power_type, Charger.PowerType.AC)
		self.assertEqual(charger.max_power_kw, 22)

	def test_vehicle_can_be_added_and_edited(self):
		response = self.client.post(reverse('operations:vehicle_create'), {
			'manufacturer': self.manufacturer.pk, 'model_name': 'Seal', 'trim': 'Premium',
			'slug': 'operations-seal', 'model_year': '2025', 'body_style': 'Sedan',
			'description': 'Sourced vehicle listing.', 'price': '650000', 'currency': 'GHS',
			'availability': 'enquire', 'range_km': '500', 'battery_kwh': '80',
			'max_charging_kw': '150', 'connector_type': 'CCS2', 'power_kw': '300',
			'seating': '5', 'is_demo': 'on', 'is_featured': 'on', 'is_published': 'on',
		})
		self.assertRedirects(response, reverse('operations:vehicles'))
		vehicle = Vehicle.objects.get(slug='operations-seal')
		response = self.client.post(reverse('operations:vehicle_edit', args=[vehicle.pk]), {
			'manufacturer': self.manufacturer.pk, 'model_name': 'Seal', 'trim': 'Updated',
			'slug': 'operations-seal', 'model_year': '2025', 'body_style': 'Sedan',
			'description': 'Sourced vehicle listing.', 'price': '650000', 'currency': 'GHS',
			'availability': 'available', 'range_km': '500', 'battery_kwh': '80',
			'max_charging_kw': '150', 'connector_type': 'CCS2', 'power_kw': '300',
			'seating': '5', 'is_demo': 'on', 'is_featured': 'on', 'is_published': 'on',
		})
		self.assertRedirects(response, reverse('operations:vehicles'))
		vehicle.refresh_from_db()
		self.assertEqual(vehicle.availability, Vehicle.Availability.AVAILABLE)
		self.assertEqual(vehicle.trim, 'Updated')

	def test_payments_are_review_only(self):
		response = self.client.get(reverse('operations:payments'))
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, 'Add record')

	def test_fault_can_be_created_and_resolved(self):
		response = self.client.post(reverse('operations:fault_create'), {
			'station': self.station.pk, 'charger': '', 'title': 'Connector inspection',
			'description': 'Inspect the connector housing.', 'severity': 'high', 'status': 'open',
		})
		self.assertRedirects(response, reverse('operations:faults'))
		fault = FaultReport.objects.get(title='Connector inspection')
		self.assertEqual(fault.reported_by, self.user)
		response = self.client.post(reverse('operations:fault_edit', args=[fault.pk]), {
			'station': self.station.pk, 'charger': '', 'title': fault.title,
			'description': fault.description, 'severity': 'high', 'status': 'resolved',
		})
		self.assertRedirects(response, reverse('operations:faults'))
		fault.refresh_from_db()
		self.assertIsNotNone(fault.resolved_at)

	def test_maintenance_can_be_scheduled(self):
		response = self.client.post(reverse('operations:maintenance_create'), {
			'station': self.station.pk, 'charger': '', 'assigned_to': '',
			'title': 'Quarterly site inspection', 'notes': 'Check service equipment.',
			'scheduled_for': '2026-12-15T10:00', 'status': 'scheduled', 'completed_at': '',
		})
		self.assertRedirects(response, reverse('operations:maintenance'))
		self.assertTrue(MaintenanceRecord.objects.filter(title='Quarterly site inspection').exists())

	def test_view_only_staff_does_not_see_edit_controls(self):
		Vehicle.objects.create(
			manufacturer=self.manufacturer, model_name='Read Only EV', slug='read-only-ev',
			description='Test listing.', is_published=True,
		)
		viewer = get_user_model().objects.create_user(username='inventory-viewer', is_staff=True)
		viewer.user_permissions.add(Permission.objects.get(codename='view_vehicle', content_type__app_label='vehicles'))
		self.client.force_login(viewer)
		response = self.client.get(reverse('operations:vehicles'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Read Only EV')
		self.assertNotContains(response, 'Add record')
		self.assertNotContains(response, 'vehicle_edit')
