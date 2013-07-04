from django.test import TestCase
from django.core.urlresolvers import reverse

class DashboardTest(TestCase):
    def test_dashboard_index(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_favorites(self):
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_settings(self):
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_billing(self):
        response = self.client.get(reverse('billing'))
        self.assertEqual(response.status_code, 302)




