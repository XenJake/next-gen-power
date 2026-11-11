from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from apps.charging.models import Charger, ChargingStation
from apps.vehicles.models import Manufacturer, Vehicle, VehicleImage
from .models import ContactMessage


class PublicPagesTests(TestCase):
	def test_homepage_renders_new_brand(self):
		response = self.client.get(reverse('core:home'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'NEXT GEN POWER')

	def test_contact_form_persists_message(self):
		response = self.client.post(reverse('core:contact'), {
			'name': 'Ama Test',
			'email': 'ama@example.com',
			'phone': '0200000000',
			'inquiry_type': 'partnership',
			'subject': 'Charging partnership',
			'message': 'Please contact me about a site.',
		})
		self.assertRedirects(response, reverse('core:contact'))
		self.assertEqual(ContactMessage.objects.count(), 1)


class ChargingDemoSeedTests(TestCase):
	def create_previous_seed_records(self):
		ChargingStation.objects.create(
			name='Demo Labadi Beach Hotel',
			slug='demo-labadi-beach-hotel',
			address='La Road, La, Accra',
			city='Accra',
			region='Greater Accra',
			site_type=ChargingStation.SiteType.HOTEL,
			is_published=True,
			is_demo=True,
		)
		manufacturer = Manufacturer.objects.create(name='Old Demo Manufacturer')
		Vehicle.objects.create(
			manufacturer=manufacturer,
			model_name='Atto 3',
			slug='byd-atto-3-extended-range',
			description='Previous demo listing.',
			is_published=True,
			is_demo=True,
		)

	def test_demo_seed_matches_greater_accra_location_plan_idempotently(self):
		self.create_previous_seed_records()
		call_command('seed_demo_content', verbosity=0)
		call_command('seed_demo_content', verbosity=0)
		stations = ChargingStation.objects.filter(is_published=True, is_demo=True)
		expected_slugs = {
			'demo-accra-mall',
			'demo-west-hills-mall',
			'demo-atlantic-mall',
			'demo-the-junction-mall',
			'demo-palace-mall-center',
			'demo-community-25',
			'demo-one-airport-square',
		}
		self.assertEqual(stations.count(), 7)
		self.assertSetEqual(set(stations.values_list('slug', flat=True)), expected_slugs)
		self.assertTrue(all(station.region == 'Greater Accra' for station in stations))
		self.assertTrue(all(station.chargers.count() == 10 for station in stations))
		self.assertEqual(
			Charger.objects.filter(
				station__in=stations,
				power_type=Charger.PowerType.AC,
				connector_type='Type 2',
				max_power_kw=22,
			).count(),
			70,
		)
		self.assertFalse(stations.filter(site_type=ChargingStation.SiteType.HIGHWAY).exists())
		self.assertFalse(ChargingStation.objects.get(slug='demo-labadi-beach-hotel').is_published)

	def test_demo_seed_loads_drop_shipped_usd_vehicle_listings(self):
		self.create_previous_seed_records()
		call_command('seed_demo_content', verbosity=0)
		expected_prices = {
			'byd-sealion': 40000,
			'jetour-t2': 25000,
			'geely-galaxy-e5': 17000,
			'xpeng-g7': 74000,
			'tesla-model-3': 94000,
			'aito-m9': 100000,
		}
		vehicles = Vehicle.objects.filter(is_published=True)
		self.assertEqual(vehicles.count(), len(expected_prices))
		self.assertEqual(
			{vehicle.slug: int(vehicle.price) for vehicle in vehicles},
			expected_prices,
		)
		self.assertTrue(all(vehicle.currency == 'USD' for vehicle in vehicles))
		self.assertTrue(all(not vehicle.is_demo for vehicle in vehicles))
		self.assertFalse(Vehicle.objects.get(slug='byd-atto-3-extended-range').is_published)
		self.assertEqual(VehicleImage.objects.filter(vehicle__in=vehicles).count(), 30)
		self.assertTrue(all(vehicle.images.count() == 5 for vehicle in vehicles))
		self.assertTrue(all(
			image.image_url and image.local_path and image.source_url and image.credit and image.license_name and image.license_url
			for image in VehicleImage.objects.filter(vehicle__in=vehicles)
		))
		self.assertContains(self.client.get(reverse('vehicles:catalogue')), '$40,000')
		self.assertContains(
			self.client.get(reverse('vehicles:detail', args=['byd-sealion'])),
			'$40,000',
		)
		detail = self.client.get(reverse('vehicles:detail', args=['byd-sealion']))
		self.assertEqual(detail.content.decode().count('data-gallery-open'), 5)
		self.assertContains(detail, 'Photo by Agratsa')
		self.assertContains(detail, 'CC BY 3.0')
