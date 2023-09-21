from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from AppUser.models import CustomUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "phone_number"]
