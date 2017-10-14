from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.urls import resolve
from django.test import TestCase
from django.core import mail
from ..tokens import account_activation_token

from ..views import signup
from ..forms import SignUpForm


class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('home:signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        '''
        The view must contain 15 inputs: csrf, username, first_name, last_name, birth_day,
        email, password1, password2, submit
        and 6 language localization inputs
        '''
        self.assertContains(self.response, '<input', 15)
        self.assertContains(self.response, 'type="text"', 4)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('home:signup')
        data = {
            'username': 'john',
            'email': 'john@doe.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home:home-login')

    def test_redirection(self):
        '''
        A valid form submission should redirect the user to the home page
        '''
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


class SignupConfirmTests(TestCase):
    def setUp(self):
        url = reverse('home:signup')
        data = {
            'username': 'john',
            'email': 'john@doe.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.client.post(url, data)
        self.home_url = reverse('home:home-login')
        self.user = User.objects.get(username='john')
        
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)
        url = reverse('home:activate', kwargs={'uidb64': uid, 'token': token})

        self.response = self.client.post(url, {})

    def test_redirection(self):
        '''
        A valid form submission should redirect the user to 'signup' view
        '''
        self.assertRedirects(self.response, self.home_url)

    def test_user_authentication(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have an `user` to its context, after a successful sign up.
        '''
        response = self.client.get(self.home_url)
        self.assertTrue(self.user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('home:signup')
        self.response = self.client.post(url, {})  # submit an empty dictionary

    def test_signup_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())