from django.core import mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase


class PasswordResetMailTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='john', email='john@mail.com', password='123')
        self.response = self.client.post(reverse('home:password_reset'), { 'email': 'john@mail.com' })
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual('TestSite password reset'.strip(), self.email.subject.strip())

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('home:password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('john', self.email.body)

    def test_email_to(self):
        self.assertEqual(['john@mail.com',], self.email.to)