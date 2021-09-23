from django.shortcuts import render
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
# Create your views here.


class RegisterForm (UserCreationForm):
    # UserCreationForm comes with username, password1, password2 as default

    # add additional fields
    first_name = forms.CharField(label="Enter First Name")  # first name field
    last_name = forms.CharField(label="Enter Last Name")  # last name field
    # use email as username field
    email = forms.EmailField(label="Enter E-mail")

    def clean_email(self):
        cleaned_email = self.cleaned_data.get('email').lower()
        # makes sure emails are unique
        if User.objects.filter(email=cleaned_email).exists():
            raise ValidationError("A user with that email already exists")
        return cleaned_email

    class Meta:
        model = User  # based on User model

        # layout where want fields to be, type in order you want it to appear
        fields = ["first_name", "last_name", "email",
                  "username",  "password1", "password2"]


class AddClassForm (forms.Form):
    school = forms.ChoiceField(choices=[(
        'san jose state university', 'San Jose State University'), ('uc berkeley', 'UC Berkeley')])
    class_taken = forms.CharField(label="Classes Taken", required=False)


class AddTutorTimeForm (forms.Form):
    day_of_week = forms.ChoiceField(label='Day of Week', required=False, choices=[('sunday', 'Sunday'), (
        'monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday')])
