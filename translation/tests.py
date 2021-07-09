import json

from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .views import TranslateView
from .models import EnglishToHindiTranslation, MLRequest, Endpoint, MLAlgorithm
from rest_framework import status

# Create your tests here.
translate_url = reverse('translate', args=['translate'])


class UrlTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        endpoint = Endpoint.objects.create(name='Translate', owner='Admin')
        mlalgo = MLAlgorithm.objects.create(name='TestAlgo', description='None', code='None', version=1.0,
                                        owner='Admin', parent_endpoint=endpoint)
    def test_url_with_bad_info(self):
        translate_url = reverse('translate', args=['None'])
        payload = {'full_name': 'Tanmay'}
        response = self.client.post(translate_url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_url_with_correct_info(self):
        translate_url = reverse('translate', args=['translate'])
        payload = {'full_name': 'Tanmay', 'address': '', 'relation_name': ''}
        response = self.client.post(translate_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TranslateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        endpoint = Endpoint.objects.create(name='Translate', owner='Admin')
        mlalgo = MLAlgorithm.objects.create(name='TestAlgo', description='None', code='None', version=1.0,
                                            owner='Admin', parent_endpoint=endpoint)

    def test_validation_of_inc_data(self):
        payload = {'full_name': 123}
        response = self.client.post(translate_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_model_saving_data(self):
        payload = {'full_name': 'Akshay Khan', 'address': 'Flat no. 11B, Gokuldham Society, Mumbai.',
                   'relation_name': 'Ajay Khan'}
        response = self.client.post(translate_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        exists = MLRequest.objects.filter(input_data__contains='Akshay Khan').exists()
        self.assertTrue(exists)
