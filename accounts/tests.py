"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import Client
from django.test import TestCase
from django.conf import settings
from django.utils.timezone import now

class DashboardTest(TestCase):
    def test_dashboard_index(self):
        response = self.client.get('/accounts/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_favorites(self):
        response = self.client.get('/accounts/favorites/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_settings(self):
        response = self.client.get('/accounts/settings/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_billing(self):
        response = self.client.get('/accounts/billing/')
        self.assertEqual(response.status_code, 200)




