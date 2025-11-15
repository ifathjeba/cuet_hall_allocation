from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application, RoomApplication

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
    student_id = forms.CharField(max_length=50)  # this matches your HTML

    class Meta:
        model = RoomApplication
        exclude = ['student', 'status', 'applied_at']

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Map the HTML student_id to model field university_id
        instance.university_id = self.cleaned_data['student_id']
        if commit:
            instance.save()
        return instance
