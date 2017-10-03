from django.shortcuts import render, redirect, render_to_response
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth import login, logout, authenticate
from .forms import SignUpForm, EditProfileInfo, EditProfilePhoto
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
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView

from .tasks import send_email

class SignUp(View):
    singup_form = SignUpForm
    template_name = 'registration/signup.html'

    def get(self, request):
        form = self.singup_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.singup_form(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            # user = form.save(commit=False)
            # user.is_active = False
            # user.refresh_from_db()  # load the profile instance created by the signal
            # user.profile.email = form.cleaned_data.get('email')
            # user.profile.birth_date = form.cleaned_data.get('birth_date')
            # user.profile.first_name = form.cleaned_data.get('first_name')
            # user.profile.last_name = form.cleaned_data.get('last_name')
            user.save()

            current_site = get_current_site(request)
            send_email.delay(user=user, current_site=current_site.domain)

            return redirect('/')
        return render(request, self.template_name, {'form': form})


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


@method_decorator(login_required, name='dispatch')
class ViewProfile(View):
    template_name = 'accounts/profile.html'

    def get(self, request, pk=None):
        if pk:
            user = User.objects.get(pk=pk)
        else:
            user = request.user

        if request.user.id == user.id:
            is_own = True
        else:
            is_own = False

        context = {'user': user, 'is_own': is_own}
        return render(request, self.template_name, context)

@login_required(login_url='/login/')
def edit_profile(request):

    if request.method == 'POST':        
        profile_form = EditProfilePhoto(request.POST, request.FILES, instance=request.user.profile)
        user_form = EditProfileInfo(request.POST, instance=request.user)

        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse('home:edit_profile'))

        if user_form.is_valid():
            user_form.save()
            return redirect(reverse('home:edit_profile'))


    else:
        profile_form = EditProfilePhoto(instance=request.user.profile)
        user_form = EditProfileInfo(instance=request.user)

    
    context = {'profile_form': profile_form, 'user_form': user_form}
    return render(request, 'accounts/edit_profile.html', context)


@method_decorator(login_required, name='dispatch')
class ChangePassword(View):
    form = PasswordChangeForm
    template_name = 'accounts/change_password.html'

    def get(self, request):
        form = self.form(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('home:view_profile'))
        return render(request, self.template_name, {'form': form})

def recommendation_list():
    # return [User.objects.get(pk=1), User.objects.get(pk=2)]
    all_users = User.objects.all().count()
    return [User.objects.get(pk=i) for i in range(1, 1 + all_users)]
