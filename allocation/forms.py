from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import RoomApplication, Profile

USER_TYPE_CHOICES = [
    ('student', 'Student'),
    ('authority', 'Hall Authority'),
]


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'user_type')

    def save(self, commit=True):
        user = super().save(commit=False)

        # auto-generate username from email
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class RoomApplicationForm(forms.ModelForm):
    class Meta:
        model = RoomApplication
        fields = [ 'year', 'cgpa', 'room_type', 'room_number', 'special_request']
        widgets = {
            'year': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'special_request': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'phone', 'gender', 'department', 'year', 'session']
