from django.test import TestCase
from django.urls import reverse

from .models import Manufacturer, Vehicle, VehicleEnquiry, VehicleImage


class VehicleCatalogueTests(TestCase):
	def setUp(self):
		self.manufacturer = Manufacturer.objects.create(name='BYD', country='China')
		self.vehicle = Vehicle.objects.create(
			manufacturer=self.manufacturer,
			model_name='Example EV',
			slug='example-ev',
			description='A test listing.',
			is_published=True,
		)

	def test_catalogue_and_detail_render(self):
		self.assertEqual(self.client.get(reverse('vehicles:catalogue')).status_code, 200)
		response = self.client.get(self.vehicle.get_absolute_url())
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Example EV')

	def test_detail_gallery_uses_this_vehicle_images_and_credits(self):
		VehicleImage.objects.create(
			vehicle=self.vehicle,
			image_url='https://thumb.wikimedia.org/example.jpg',
			local_path='images/vehicles/example-ev-1.jpg',
			source_url='https://commons.wikimedia.org/wiki/File:Example.jpg',
			alt_text='BYD Example EV exterior',
			credit='Example Photographer',
			license_name='CC BY-SA 4.0',
			license_url='https://creativecommons.org/licenses/by-sa/4.0/',
		)
		response = self.client.get(self.vehicle.get_absolute_url())
		self.assertContains(response, 'BYD Example EV exterior')
		self.assertContains(response, 'Example Photographer')
		self.assertContains(response, 'CC BY-SA 4.0')
		self.assertContains(response, 'class="vehicle-brand-name">BYD</p>')
		self.assertContains(response, 'data-full-src="/static/images/vehicles/example-ev-1.jpg"')
		self.assertContains(response, '<dialog class="gallery-lightbox"')
		self.assertNotContains(response, 'target="_blank" rel="noopener"><img')

	def test_vehicle_enquiry_is_saved_against_listing(self):
		response = self.client.post(self.vehicle.get_absolute_url(), {
			'name': 'Kojo Test',
			'email': 'kojo@example.com',
			'phone': '0240000000',
			'message': 'Please send details.',
		})
		self.assertRedirects(response, self.vehicle.get_absolute_url())
		enquiry = VehicleEnquiry.objects.get()
		self.assertEqual(enquiry.vehicle, self.vehicle)

	def test_unpublished_vehicle_is_not_public(self):
		self.vehicle.is_published = False
		self.vehicle.save()
		self.assertEqual(self.client.get(self.vehicle.get_absolute_url()).status_code, 404)

	def test_manufacturer_and_body_style_filters(self):
		Vehicle.objects.create(
			manufacturer=self.manufacturer,
			model_name='Example SUV',
			slug='example-suv',
			body_style=Vehicle.BodyStyle.SUV,
			description='Another test listing.',
			is_published=True,
		)
		response = self.client.get(reverse('vehicles:catalogue'), {'manufacturer': 'BYD', 'type': 'SUV'})
		self.assertContains(response, 'Example SUV')
		self.assertNotContains(response, 'Example EV')
