from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from home.models import Profile

class ModelTestCase(TestCase):
	"""This class defines the test suite for the User model."""
	def setUp(self):
		# self.factory = RequestFactory()
		self.u1 = User.objects.create_user(username='jacob', email='jacob@mail.com', password='top_secret')
		self.u1.save()
		# self.up1 = Profile.objects.create(user=self.u1)

	def test_model_can_create_a_user(self):
		old_count = User.objects.count()
		self.u2 = User.objects.create_user(username='jacob2', email='jacob2@mail.com', password='top_secret')
		self.u2.save()
		new_count = User.objects.count()
		self.assertNotEqual(old_count, new_count)
		self.assertNotEqual(self.u1, self.u2)

