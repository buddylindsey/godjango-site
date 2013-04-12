"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import Client
from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse

class DashboardTest(TestCase):
    def test_dashboard_index(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_favorites(self):
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_settings(self):
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_billing(self):
        response = self.client.get(reverse('billing'))
        self.assertEqual(response.status_code, 200)




