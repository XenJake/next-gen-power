from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from apps.charging.models import Charger, ChargingStation
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
	def test_demo_seed_matches_location_and_charger_plan_idempotently(self):
		call_command('seed_demo_content', verbosity=0)
		call_command('seed_demo_content', verbosity=0)
		stations = ChargingStation.objects.filter(is_published=True, is_demo=True)
		mall_hotel_office = stations.exclude(site_type=ChargingStation.SiteType.HIGHWAY)
		highway_sites = stations.filter(site_type=ChargingStation.SiteType.HIGHWAY)
		self.assertEqual(stations.count(), 7)
		self.assertEqual(mall_hotel_office.count(), 5)
		self.assertTrue(all(station.chargers.count() == 10 for station in mall_hotel_office))
		self.assertEqual(Charger.objects.filter(station__in=mall_hotel_office, power_type=Charger.PowerType.AC, connector_type='Type 2', max_power_kw=22).count(), 50)
		self.assertEqual(Charger.objects.filter(station__in=highway_sites, power_type=Charger.PowerType.DC, connector_type='CCS2', max_power_kw=88).count(), 5)
		self.assertEqual(highway_sites.get(slug='demo-accra-kumasi-suhum').chargers.count(), 3)
		self.assertEqual(highway_sites.get(slug='demo-accra-cape-coast-winneba').chargers.count(), 2)
