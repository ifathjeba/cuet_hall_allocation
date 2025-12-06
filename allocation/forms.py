from django import forms
from .models import RoomApplication,Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


USER_TYPE_CHOICES = [
    ('student', 'Student'),
    ('authority', 'Hall Authority'),
]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['student_id', 'phone', 'gender', 'department', 'year', 'session']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
        }


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
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
            'hall': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your room number'}),
        }
