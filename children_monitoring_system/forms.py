from django import forms
from .models import User
# from django.contrib.auth.forms import UserCreationForm
# from django.core.exceptions import ValidationError
import re

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Username',
            'id': 'username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password',
            'id': 'password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'remember_me'
        })
    )

class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Username',
            'id': 'username'
        })
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password',
            'id': 'password'
        }), 
        label="Password"
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Confirm Password',
            'id': 'confirm_password'
        }), 
        label="Confirm Password"
    )
    full_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Full Name',
            'id': 'full_name'
        }), 
        label='Full Name'
    )
    email = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Email',
            'id': 'email'
        }), 
        label='Email'
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'full_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        email = cleaned_data.get('email')
        full_name = cleaned_data.get('full_name')

        # Username validation
        if not username:
            self.add_error('username', "Username is required.")
        elif username and (len(username) < 8 or len(username) > 15):
            self.add_error('username', "Username must be between 8 and 15 characters long.")
        elif User.objects.filter(username=username).exists():
            self.add_error('username', "Username has been taken.")

        # Email validation
        if not email:
            self.add_error('email', "Email is required.")
        elif not self.is_valid_email(email):
            self.add_error('email', "Enter a valid email address.")
        elif User.objects.filter(email=email).exists():
            self.add_error('email', "Email has been taken.")

        # Custom password validation for complexity
        if not password:
            self.add_error('password', "Password is required.")
        elif password:
            if (len(username) < 8):
                self.add_error('password', "Password must be at least 8 characters long.")
            elif not any(char.isdigit() for char in password):
                self.add_error('password', "Password must contain at least one number.")
            elif not any(char.isalpha() for char in password):
                self.add_error('password', "Password must contain at least one letter.")

        if not confirm_password:
            self.add_error('confirm_password', "Confirm password is required.")
        elif password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        if not full_name:
            self.add_error('full_name', "Full name is required.")
        elif not re.match(r'^[A-Za-z\s]+$', full_name):
            self.add_error('full_name', "Full name must contain only letters and spaces.")
        return cleaned_data
    
    def is_valid_email(self, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user