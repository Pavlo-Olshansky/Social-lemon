from django.shortcuts import render, redirect, render_to_response
from django.views.generic.base import TemplateView
from django.contrib.auth import login, logout, authenticate
from .forms import SignUpForm, EditProfileInfo, EditProfilePhoto, EditProfileAdditionalInfo
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.http import JsonResponse
from django.template.loader import render_to_string

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            # user = form.save(commit=False)
            # user.is_active = False
            # user.refresh_from_db()  # load the profile instance created by the signal
            # user.profile.email = form.cleaned_data.get('email')
            # user.profile.birth_date = form.cleaned_data.get('birth_date')
            # user.profile.first_name = form.cleaned_data.get('first_name')
            # user.profile.last_name = form.cleaned_data.get('last_name')
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/')
    else:
        return render(request, 'registration/account_activation_invalid.html')

def account_activation_sent(request):
    return render(request, 'home.html')


@login_required(login_url='/login/')
def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user

    if request.user.id == user.id:
        is_own = True
    else:
        is_own = False

    context = {'user': user, 'is_own': is_own}
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='/login/')
def edit_profile(request):

    if request.method == 'POST':        
        profile_form = EditProfilePhoto(request.POST, request.FILES, instance=request.user.profile)
        user_form = EditProfileInfo(request.POST, instance=request.user)
        additional_form = EditProfileAdditionalInfo(request.POST, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse('home:edit_profile'))

        if user_form.is_valid():
            user_form.save()
            return redirect(reverse('home:edit_profile'))

        if additional_form.is_valid():
            additional_form.save()
            return redirect(reverse('home:edit_profile'))

    else:
        profile_form = EditProfilePhoto(instance=request.user.profile)
        user_form = EditProfileInfo(instance=request.user)
        additional_form = EditProfileAdditionalInfo(instance=request.user.profile)

    
    context = {'profile_form': profile_form, 'user_form': user_form, 'additional_form': additional_form}
    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('home:view_profile'))
    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)

def recommendation_list():
    # return [User.objects.get(pk=1), User.objects.get(pk=2)]
    all_users = User.objects.all().count()
    return [User.objects.get(pk=i) for i in range(1, 1 + all_users)]
