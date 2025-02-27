from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            occupation='Tester'
        )
        self.token = Token.objects.create(user=self.user)
    
    def test_signup(self):
        url = '/signup/'
        data = {
            'username': 'newuser',
            'password': 'newpass',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'occupation': 'New Occupation'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'newuser')

    # def test_login_view(self):
    #     url = '/login/'
    #     data = {
    #         'email': 'testuser@example.com',
    #         'password': 'testpass'
    #     }
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn('token', response.data)

    # def test_get_current_user(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    #     url = '/get_current_user/'
    #     response = self.client.get(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['email'], 'testuser@example.com')

    # def test_update_current_user(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    #     url = '/update_current_user/'
    #     data = {
    #         'first_name': 'Updated',
    #         'last_name': 'User'
    #     }
    #     response = self.client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['first_name'], 'Updated')

    # def test_logout_view(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    #     url = '/logout/'
    #     response = self.client.post(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['success'], 'Logged out successfully')
