from django.test import TestCase
from django.urls import reverse

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
