from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User

# Create your tests here.

class AuthTests(APITestCase):

    def setUp(self):
        # This setup run creates a test database user before each test runs
        self.register_url = reverse('auth_register')
        self.login_url = reverse('token_obtain_pair')

        self.user_data = {
            "email": "teststudent@lms.com",
            "username": "teststudent",
            "password": "securepassword123",
            "role": "STUDENT"
        }

        # Pre-seed one user for testing the login endpoint directly
        self.existing_user = User.objects.create_user(
            username="existinguser",
            email="existing@lms.com",
            password="loginpassword123",
            role="STUDENT"
        )

    def test_user_registration_via_api(self):
        """
        Verify that a user can successfully register an account through the API.
        """
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "User registered successfully!")

    def test_user_login_returns_jwt_tokens(self):
        """
        Verify that correct credentials successfully return access and refresh JWT tokens.
        """
        login_data = {
            "email": "existing@lms.com",  # Remember simple JWT maps email to username key
            "password": "loginpassword123"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
