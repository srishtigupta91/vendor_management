import logging

import pytest
from rest_framework.test import APIClient, APITestCase
from vendor import models as vendor_models
from vendor.models import Vendors

client = APIClient()


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()



class TestVendorPerformance(APITestCase):
    """ Test the vendor performance based on the orders purchased"""

    pytestmark = pytest.mark.django_db

    def user_authentication(self):
        payload = {"username": "admin", "password": "admin@123"}
        client.post("/auth/users/create/", data=payload)
        response = client.post("/auth/custom-token-auth/", data=payload)
        return response.json()['token']

    def test_create_vendors(self):
        payload = {"vendor_name": "IBM Think Pad", "vendor_code": "ThinkPad1001", "contact_number": "+918826346669", "address": "Kormangala, Bangalore"}
        headers = {"Authorization": "Token {}".format(self.user_authentication())}
        response = self.client.post('/api/vendors/', data=payload, headers=headers, format="json")
        self.assertEqual(response.status_code, 201)

    def test_vendor_performance(self):
        self.test_create_vendors()
        vendor_id = Vendors.objects.last().id
        response = client.get("/api/vendors/{}/performance/".format(vendor_id))
        assert response.status_code == 200
        assert response.json()['vendor_id'] == 1
