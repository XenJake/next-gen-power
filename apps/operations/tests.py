from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse


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
		permission = Permission.objects.get(
			codename='view_chargingsession',
			content_type__app_label='charging',
		)
		self.user.user_permissions.add(permission)
		self.client.force_login(self.user)
		response = self.client.get(reverse('operations:dashboard'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Network overview')
