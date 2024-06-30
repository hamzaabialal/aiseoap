from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import SignupModel
class SignUpForm(UserCreationForm):

    class Meta:
        model = SignupModel
        fields = ['username', 'full_name', 'email', 'password', 'confirm_password']
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'}),
                   'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.TextInput(attrs={'class': 'form-control'}),
                   'password': forms.PasswordInput(attrs={'class': 'form-control'}),
                      'confirm_password': forms.PasswordInput(attrs={'class': 'form-control'}),}

        def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data.get("password1")
            confirm_password = cleaned_data.get("password2")

            if password and confirm_password and password != confirm_password:
                raise forms.ValidationError("Passwords do not match")

            return cleaned_data
