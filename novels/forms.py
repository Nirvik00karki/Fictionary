from django import forms
from novels.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
