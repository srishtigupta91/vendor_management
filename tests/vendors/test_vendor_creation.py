import logging

import pytest
from rest_framework.test import APIClient, APITestCase

client = APIClient()


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestVendorCreation(APITestCase):
    """ Vendor creation through model view set test case """

    pytestmark = pytest.mark.django_db

    def user_authentication(self):
        payload = {"username": "admin", "password": "admin@123"}
        client.post("/auth/users/create/", data=payload)
        response = client.post("/auth/api-token-auth/", data=payload)
        return response.json()['token']

    def test_create_vendors(self):
        payload = {"vendor_name": "IBM Think Pad", "vendor_code": "ThinkPad1001", "contact_number": "+918826346669", "address": "Kormangala, Bangalore"}
        headers = {"Authorization": "Token {}".format(self.user_authentication()), "Content-Type": "application/json"}
        response = self.client.post('/api/vendors/', data=payload, headers=headers, format="json")
        self.assertEqual(response.status_code, 201)

    def test_vendor_code_validation(self):
        self.test_create_vendors()
        payload = {"vendor_name": "IBM Think Pad", "vendor_code": "ThinkPad1001", "contact_number": "+918826345562",
                   "address": "Kormangala, Bangalore"}
        headers = {"Authorization": "Token {}".format(self.user_authentication()), "Content-Type": "application/json"}
        response = client.post('/api/vendors/', data=payload,headers=headers, format="json")
        assert response.status_code == 400
        assert response.json()['vendor_code'] == ["vendors with this vendor code already exists."]

    def test_contact_number_validation(self):
        self.test_create_vendors()
        payload = {"vendor_code": "1008", "vendor_name": "IBM001", "contact_number": "9827676761", "address": "Mumbai Maharastra"}
        headers = {"Authorization": "Token {}".format(self.user_authentication()), "Content-Type": "application/json"}
        response = client.post("/api/vendors/", data=payload, headers=headers, format="json")
        assert response.status_code == 400
        assert response.json()['contact_number'] == ['The phone number entered is not valid.']

    def test_vendor_name_validation(self):
        self.test_create_vendors()
        payload = {"vendor_name": "IBM Think Pad", "vendor_code": "ThinkPad1001", "contact_number": "+918826345562",
                   "address": "Kormangala, Bangalore"}
        headers = {"Authorization": "Token {}".format(self.user_authentication())}
        response = client.post("/api/vendors/", data=payload, headers=headers, format="json")
        assert response.status_code == 400
        assert response.json()['vendor_name'] == ["Vendor already exists with this vendor name!!!"]
