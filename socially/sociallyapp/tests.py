from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import User

class LoginLogoutTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            username='testuser'
        )

    def test_login_user(self):
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'testpassword'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_login_user_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_user(self):
        # Login to get a refresh token
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'testpassword'
        })

        # Get the refresh token from the login response
        refresh_token = response.data['refresh']

        # Logout with the refresh token
        response = self.client.post(reverse('logout'), json={'refresh_token': refresh_token})
        #print(self.client._session.request)
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)