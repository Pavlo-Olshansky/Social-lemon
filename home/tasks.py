from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token

from celery import shared_task

@shared_task
def send_email(user, current_site):
	subject = 'Activate Your MySite Account'
	message = render_to_string('registration/account_activation_email.html', {
	    'user': user,
	    'domain': current_site,
	    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
	    'token': account_activation_token.make_token(user),
	})
	user.email_user(subject, message)
