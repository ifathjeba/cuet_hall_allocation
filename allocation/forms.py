from django import forms
from .models import RoomApplication
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

USER_TYPE_CHOICES = [
    ('student', 'Student'),
    ('authority', 'Hall Authority'),
]

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')


class RoomApplicationForm(forms.ModelForm):
    class Meta:
        model = RoomApplication
        exclude = ['status', 'applied_at']
