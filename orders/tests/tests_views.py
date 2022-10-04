import json
from urllib import response
from django.urls import reverse

from rest_framework.test import APITestCase, APIRequestFactory

from orders.models import Order, Item
from orders.serializers import OrderSerializer, ItemSerializer
from orders.views import OrderApiView


class OrderApiViewTestCase(APITestCase):

    def setUp(self) -> None:
        self.url = reverse("orders:order_list")
        for i in range(30):
            test_object = {
                "loading_point": f"Warsaw {i}",
                "unloading_point": f"Krakow {i}",
                "load_date": "2022-09-30",
                "unload_date": "2023-11-20",
                "status": "load",
                "items": []
            }
            self.client.post(self.url, json.dumps(test_object),
                             content_type='application/json')

    def test_list(self):
        response = self.client.get(self.url, content_type='application/json')
        self.assertEqual(response.status_code, 200, 'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_list_pagination(self):
        response = self.client.get(self.url, content_type='application/json')
        self.assertEqual(response.status_code, 200, 'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))
        self.assertTrue('count' in response.data)
        self.assertTrue(response.data.get('count') == 30)
        self.assertEqual(len(response.data.get('results')), 10)

    def test_create(self):
        test_object = {
            "loading_point": "Minsk",
            "unloading_point": "Gdansk",
            "load_date": "2022-09-29",
            "unload_date": "2022-11-20",
            "status": "load",
            "items": []
        }
        response = self.client.post(self.url, json.dumps(
            test_object), content_type='application/json')
        self.assertEqual(response.status_code, 201, 'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_create_with_items(self):
        test_object = {
            "loading_point": "Minsk",
            "unloading_point": "Gdansk",
            "load_date": "2022-09-29",
            "unload_date": "2022-11-20",
            "status": "load",
            "items": [{"name": "test", "description": "Something useful", "quantity": 12},
                      {"name": "test 2", "description": "Something useful", "quantity": 12}]
        }
        response = self.client.post(self.url, json.dumps(
            test_object), content_type='application/json')
        self.assertEqual(response.status_code, 201, 'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_create_wrong_data(self):
        test_object = {
            "loading_point": "",
            "load_date": "2022-09-29",
            "unload_date": "2022-11-20",
            "status": "load",
            "items": [{"name": "test", "description": "Something useful", "quantity": 12},
                      {"name": "test 2", "description": "Something useful", "quantity": 12}]
        }
        response = self.client.post(self.url, json.dumps(
            test_object), content_type='application/json')
        self.assertEqual(response.status_code, 400, 'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

class OrderDetailApiViewestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("orders:order_list")
        self.test_object = {
            "loading_point": "Warsaw",
            "unloading_point": "Krakow",
            "load_date": "2022-09-30",
            "unload_date": "2023-11-20",
            "status": "load",
            "items": []
        }
        self.client.post(self.url, json.dumps(
            self.test_object), content_type='application/json')

        self.test_object = {
            "loading_point": "Warsaw",
            "unloading_point": "Krakow",
            "load_date": "2022-09-30",
            "unload_date": "2023-11-20",
            "status": "load",
            "items": [{"name": "test", "description": "Something useful", "quantity": 12},
                      {"name": "test 2", "description": "Something useful", "quantity": 12}]
        }
        self.client.post(self.url, json.dumps(
            self.test_object), content_type='application/json')

    def test_retrieve(self):
        response = self.client.get('/api/1/', content_type='application/json')
        self.assertEqual(response.status_code, 200, 'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_update(self):
        response = self.client.get('/api/1/', content_type='application/json')
        response.data.status = "EDITED"
        response = self.client.put('/api/1/', json.dumps(
            response.data), content_type='application/json')
        self.assertEqual(response.status_code, 200, 'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_update_wrong_data(self):
        response = self.client.get('/api/1/', content_type='application/json')
        response.data.pop('status')
        response = self.client.put('/api/1/', json.dumps(
            response.data), content_type='application/json')
        self.assertEqual(response.status_code, 400, 'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_update_with_items(self):
        response = self.client.get('/api/2/', content_type='application/json')
        items= response.data.get('items')
        response.data.status = "EDITED"
        items[0]['name'] = "EDITED 2"
        items.append({"name": "test 3", "description": "Something useful", "quantity": 12})
        response.data['items'] = items
        response = self.client.put('/api/2/', json.dumps(
            response.data), content_type='application/json')
        self.assertEqual(response.status_code, 200, 'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_delete(self):
        response = self.client.delete('/api/2/', content_type='application/json')
        self.assertEqual(response.status_code, 204, 'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))
    
    def test_delete_wrong_id(self):
        response = self.client.delete('/api/10/', content_type='application/json')
        self.assertEqual(response.status_code, 404, 'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))
