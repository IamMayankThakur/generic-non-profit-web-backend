from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory,APISimpleTestCase,APITestCase
import api.models as models
# Create your tests here.

#factory = APIRequestFactory()
USERNAME = 'tester1'
EMAIL = 'tester1@test.com'
PASSWORD = 'password'

class RefreshTokenTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(USERNAME,EMAIL,PASSWORD)
        self.url = '/api/token/'

    def test_refresh_token_fetch(self):
        response = self.client.post(self.url,{'username':USERNAME,'password':PASSWORD})
        self.assertEqual(response.status_code,200)
        #print(response.data)
        token = response.data['refresh']
        #print(f'refresh token is: {token}')
        

    def tearDown(self):
        user = User.objects.get(username = USERNAME)
        user.delete()


class AccessTokenTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(USERNAME,EMAIL,PASSWORD)
        self.url = '/api/token/refresh/'
        self.refresh_token = self.client.post('/api/token/',{'username':USERNAME,'password':PASSWORD}).data['refresh']

    def test_access_token_fetch(self):
        response = self.client.post(self.url,{'refresh': self.refresh_token})
        print(self.client.__dict__)
        self.assertEqual(response.status_code,200)
    
    def tearDown(self):
        user = User.objects.get(username = USERNAME)
        user.delete()


class HelloViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(USERNAME, email = EMAIL, password = PASSWORD)
        self.url = '/api/v1/hello/'
        self.response = self.client.post('/api/token/',{'username':USERNAME,'password':PASSWORD})
        self.refresh_token = self.response.data['refresh']
        self.access_token = self.response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + self.access_token)
    
    def test_get_event(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
    
    def tearDown(self):
        user = User.objects.get(username = USERNAME)
        user.delete()

class EventsByDateViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(USERNAME, email = EMAIL, password = PASSWORD)
        self.url = '/api/v1/get_events/'
        self.response = self.client.post('/api/token/',{'username':USERNAME,'password':PASSWORD})
        self.refresh_token = self.response.data['refresh']
        self.access_token = self.response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + self.access_token)
    
    def test_get_event(self):
        response = self.client.get(self.url,{'startDate':'2000-01-01','endDate':'2020-01-01'})
        #print(response.content)
        self.assertEqual(response.status_code,200)
    
    def tearDown(self):
        user = User.objects.get(username = USERNAME)
        user.delete()
