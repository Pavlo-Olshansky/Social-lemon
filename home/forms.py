# from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


from PIL import Image
from django import forms
from django.core.files import File
from django.forms.widgets import FileInput

from django.utils.translation import gettext_lazy as _


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        user.save()

        return user

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(label=_('Username'), widget=TextInput(attrs={'class':'validate','placeholder': 'Nickname'}))
    password = forms.CharField(label=_('Password'), widget=PasswordInput(attrs={'placeholder':'Password'}))


class EditProfileInfo(forms.ModelForm):
    # first_name = forms.CharField(label=_('First name'), required=False)
    # last_name = forms.CharField(label=_('Last name'), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name')



class EditProfilePhoto(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    file = forms.FileField(widget=FileInput)


    class Meta:
        model = Profile
        fields = ('file', 'x', 'y', 'width', 'height')

    def save(self):
        photo = super(EditProfilePhoto, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')


        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo
