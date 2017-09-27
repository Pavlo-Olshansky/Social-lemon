from django.test import TestCase

from ..forms import SignUpForm

class SignUpFormTest(TestCase):
	def test_form_has_field(self):
		form = SignUpForm()
		expected = ['first_name', 'last_name', 'birth_date', 'email']
		actual = list(form.fields)
		self.assertSequenceEqual(expected, actual)
