from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import reverse
from users.forms import RegisterForm, LoginForm

# RegisterForm test
class RegisterViewTests(TestCase):
    def setUp(self):
        self.register_url = reverse('users:register')
        self.user = {
            'email':'123@gmail.com',
            'username': 'weiwei123',
            'first_name':'wei',
            'last_name':'xuan',
            'password1':'123Frivolous',
            'password2':'123Frivolous',
        }

        self.user_shortpassword = {
            'email':'123@gmail.com',
            'first_name':'wei',
            'username': 'weiwei123',
            'last_name':'xuan',
            'password1':'1234',
            'password2':'1234',
        }

        self.user_passwords_unmatched = {
            'email':'123@gmail.com',
            'username': 'weiwei123',
            'first_name':'wei',
            'last_name':'xuan',
            'password1':'123Frivolous',
            'password2':'12345680A',
        }

    def test_register_page_url(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/register.html')

    def test_valid_form(self):
        form = RegisterForm(data=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertRedirects(
            response, '/user/login/', 
            status_code=302, target_status_code=200)

    def test_password_too_short(self):
        form = RegisterForm(data=self.user_shortpassword)
        response = self.client.post(self.register_url, self.user_shortpassword, format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(form.errors), 1)

    def test_passwords_not_matched(self):
        response = self.client.post(
            self.register_url, self.user_passwords_unmatched, 
            follow=True, format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, 'form', 
            'password2', 'Passwords do not match')

    def test_email_username_exists(self):
        self.client.post(self.register_url, self.user, format='text/html')
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertFormError(
            response, 'form', 
            'email', 'Email address already exists')
        self.assertFormError(
            response, 'form', 
            'username', 'Username already exists')

    
# LoginForm test
class LoginViewTests(TestCase):

    def setUp(self):
        self.login_url = reverse('users:login')
        self.username = "weiwei123"
        self.email = "weiwei123@gmail.com"
        self.password1 = "123Frivolous"
        self.password2 = "123Frivolous"
        self.first_name = "Wei"
        self.last_name = "Xuan"
        self.new_user = User.objects.create_user(
            self.username, self.email, self.password1,
            first_name = self.first_name,
            last_name = self.last_name
        )

        self.user = {
            'username': self.username,
            'password': self.password1,
        }
        
        self.wrong_password = {
            'username': self.username,
            'password': '123',
        }

        self.invalid_username = {
            'username': '123', 
            'password': '123',
        }

    def test_login_page_url(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/login.html')

    def test_valid_form(self):
        form = LoginForm(data=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_login_success(self):
        user = User.objects.filter(email=self.email, username=self.username)
        login = self.client.login(username=self.user['username'], password=self.user['password'])
        # Check whether user exists in DB
        self.assertIsNotNone(user)
        # Check whether user is able to login
        self.assertTrue(login)

    def test_login_invalid_username(self):
        user = User.objects.filter(username=self.invalid_username['username'])
        unsuccessful_login = self.client.login(
            username=self.invalid_username['username'],
            password=self.invalid_username['password'])
        self.assertEqual(user.count(), 0)
        self.assertFalse(unsuccessful_login)

    def test_login_incorrect_password(self):
        user = User.objects.filter(email=self.email, username=self.username)
        incorrect_password = self.client.login(
            username=self.wrong_password['username'], 
            password=self.wrong_password['password'])
        self.assertEqual(user.count(), 1)
        self.assertFalse(incorrect_password)
        self.assertIsNone(authenticate(
            username=self.wrong_password['username'],
            password=self.wrong_password['password']))


class ResetPasswordViewTests(TestCase):
    def setUp(self):
        self.reset_password = reverse('users:reset_password')
        self.reset_password_sent = reverse('users:reset_password_sent')
        self.password_reset_complete = reverse('users:password_reset_complete')

    def test_reset_password_page_url(self):
        response = self.client.get(self.reset_password)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/reset_password.html')

    def test_reset_password_sent_page_url(self):
        response = self.client.get(self.reset_password_sent)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/reset_password_sent.html')

    def test_password_reset_complete_page_url(self):
        response = self.client.get(self.password_reset_complete)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/password_reset_complete.html')