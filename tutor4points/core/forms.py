from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, School, Tutor_Info

# Create your views here.


class RegisterForm (UserCreationForm):

    # get school names from School model
    school = forms.ModelChoiceField(queryset=School.objects.all())

    class Meta:
        model = User  # based on User model

        # layout where want fields to be, type in order you want it to appear
        fields = ("first_name", "last_name", "school", "email",
                  "username", "password1", "password2")


class ProfilePicUploadForm (forms.ModelForm):

    class Meta:
        model = User
        fields = ('profile_pic',)


class UpdateTutorProfileForm (forms.ModelForm):

    class Meta:
        model = Tutor_Info
        fields = ('classes', 'times_available',
                  'timezone', 'rate', )
        widgets = {
            'times_available': forms.Textarea(attrs={
                'placeholder': 'Enter dates and times you are available to tutor (Ex: Monday 2-3pm, Wednesday 4-5pm)'}),
            'classes': forms.Textarea(attrs={
                'placeholder': 'Enter classes you have taken at your school (Ex: CS146, MATH42)'})
        }
        labels = {
            'times_available': 'Dates and Times Available to Tutor',
            'classes': 'Classes Taken'
        }
