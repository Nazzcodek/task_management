from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status

class UserViewsTest(APITestCase):  # Using APITestCase for REST Framework views
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('users:signup')
        self.login_url = reverse('users:login')

        # Create test user
        self.user_data = {'username': 'testuser', 'password': 'testpassword'}
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)

        # Authentication for API requests
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_signup_view_get(self):
        """Test the signup page loads correctly."""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_view_post_success(self):
        """Test successful user signup."""
        new_user_data = {'username': 'newuser', 'password': 'newpassword', 'password2': 'newpassword'}
        response = self.client.post(self.signup_url, new_user_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_login_view_get(self):
        """Test the login page loads correctly."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_success(self):
        """Test successful user login."""
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_user_list(self):
        """Test listing users (requires authentication)."""
        response = self.client.get(reverse('users:user-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.user.username)

    def test_get_user_info(self):
        """Test getting user information (requires authentication)."""
        response = self.client.get(reverse('users:user-get-user-info'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('users', response.data)
        self.assertIn('total', response.data)

    def test_add_user(self):
        """Test adding a new user (requires authentication)."""
        new_user_data = {'username': 'anotheruser', 'password': 'anotherpassword'} 
        response = self.client.post(reverse('users:user-create'), new_user_data, format='json')  
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['username'], new_user_data['username'])
