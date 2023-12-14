import json
import logging
from datetime import datetime

import pytest
from rest_framework.test import APIClient, APITestCase
from vendor import models as vendor_models

client = APIClient()


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()



class TestOrderCreation(APITestCase):
    """ Order creation through model view set test case """

    pytestmark = pytest.mark.django_db

    def user_authentication(self):
        payload = {"username": "admin", "password": "admin@123"}
        client.post("/auth/users/create/", data=payload)
        response = client.post("/auth/api-token-auth/", data=payload)
        return response.json()['token']

    def test_create_items(self):
        payload = {
            "serial_no": "1",
            "item_name": "Prestige Electric Kettle",
            "item_description": "1.2 Lts Prestige Electric Kettle",
            "size": "1.2 ltr  (19 cm * 18.5 cm * 21 cm)",
            "price": 654.0
        }
        headers = {"Authorization": "Token {}".format(self.user_authentication())}
        response = client.post('/api/purchase_orders/items/', data=payload, headers=headers, format="json")
        assert response.status_code == 201
        assert response.json()['serial_no'] == "1"

    def test_create_vendors(self):
        payload = {"vendor_name": "IBM Think Pad", "vendor_code": "ThinkPad1001", "contact_number": "+918826346669", "address": "Kormangala, Bangalore"}
        headers = {"Authorization": "Token {}".format(self.user_authentication())}
        response = self.client.post('/api/vendors/', data=payload, headers=headers, format="json")
        self.assertEqual(response.status_code, 201)

    def test_create_orders(self):
        self.test_create_items()
        self.test_create_vendors()
        payload = {
            "po_number": "728",
            "order_date": "2023-12-08T08:11:11.296380Z",
            "delivery_date": "2023-12-12T12:56:00Z",
            "quantity": 3,
            "status": 0,
            "issue_date": "2023-12-10T08:11:11.296533Z",
            "vendor": 1,
            "items": 1
        }
        response = client.post('/api/purchase_orders/', data=payload)
        assert response.status_code == 201
        assert response.json()['po_number'] == "728"

    def test_update_order_status(self):
        self.test_create_orders()
        payload = {
            "po_number": "728",
            "status": 1
        }
        headers = {"Authorization": "Token {}".format(self.user_authentication())}
        response = client.patch('/api/purchase_orders/728', data=payload, headers=headers, format="json")
        assert response.status_code == 200
        assert response.json()['po_number'] == "728"
