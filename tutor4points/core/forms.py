from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import PasswordInput
from .models import User, School
from crispy_forms.helper import FormHelper


# Form that allows user to create an account
class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['password1'].widget = PasswordInput(
            attrs={'placeholder': 'Password'})

        self.fields['password2'].widget = PasswordInput(
            attrs={'placeholder': 'Repeat Password'})

        self.fields['classes_taken'].required = False
        self.fields['times_available'].required = False
        self.fields['time_zone'].required = False
        self.fields['rate'].required = False

    class Meta:
        model = User  # based on User model

        # layout where want fields to be, type in order you want it to appear
        fields = ('profile_pic', "first_name", "last_name", "school", "email",
                  "username", "password1", "password2", 'school', 'is_tutor',
                  'classes_taken', 'times_available', 'time_zone', 'rate')

        widgets = {
            'first_name':
            forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name':
            forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email':
            forms.TextInput(attrs={'placeholder': 'email@address.com'}),
            'username':
            forms.TextInput(attrs={'placeholder': 'Username'}),
            'password1':
            forms.TextInput(attrs={'placeholder': 'Password'}),
            'times_available':
            forms.Textarea(attrs={
                'placeholder': 'Example: Monday 2-3pm, Wednesday 4-5pm',
                'rows': 5
            }),
            'classes_taken':
            forms.Textarea(attrs={
                'placeholder': 'Example: CS146, MATH42',
                'rows': 5
            }),
            'rate':
            forms.NumberInput(attrs={'placeholder': 'Example: 1700'})
        }

        labels = {
            'profile_pic': "Profile Picture (Optional)",
            'first_name': "First Name",
            'last_name': "Last Name",
            'is_tutor': "I want to be a tutor on Tutor4Points",
            'classes_taken': "Classes Taken",
            'times_available': "Times Available",
            'time_zone': "Time Zone",
            'rate': 'Rate (points/hour): 100 points = $1.00'
        }

    helper = FormHelper()
    helper.form_id = 'form'


# Form that allows user to update their profile_pic, first_name, last_name, school, email
# is_tutor, classes_taken, times_available, time_zone, rate
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User

        # layout where want fields to be, type in order you want it to appear
        fields = ('profile_pic', "first_name", "last_name", "school", "email",
                  'is_tutor', 'classes_taken', 'times_available', 'time_zone',
                  'rate')

        # customize placeholders
        widgets = {
            'first_name':
            forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name':
            forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'times_available':
            forms.Textarea(attrs={
                'placeholder': 'Example: Monday 2-3pm, Wednesday 4-5pm',
                'rows': 5
            }),
            'classes_taken':
            forms.Textarea(attrs={
                'placeholder': 'Example: CS146, MATH42',
                'rows': 5
            }),
            'rate':
            forms.NumberInput(attrs={'placeholder': 'Example: 1700'}),
            'profile_pic':
            forms.FileInput()
        }

        # customize form labels
        labels = {
            'profile_pic': "Profile Picture",
            'first_name': "First Name",
            'last_name': "Last Name",
            'is_tutor': "I want to be a tutor on Tutor4Points",
            'classes_taken': "Classes Taken",
            'times_available': "Times Available",
            'time_zone': "Time Zone",
            'rate': 'Rate (pts/hr): 100 points = $1.00'
        }

    helper = FormHelper()
    helper.form_id = 'form'


# Form that allows user to purchase points
# TODO rewrite form
class PurchasePointsForm(forms.ModelForm):
    class Meta:
        model = User

        # layout where want fields to be, type in order you want it to appear
        fields = ('total_points', )

        # customize placeholders
        widgets = {
            'total_points':
            forms.NumberInput(attrs={
                'placeholder': 'Example: 10000',
            })
        }

        # customize form labels
        labels = {
            'total_points': 'Enter Amount of Points to Purchase',
        }

    helper = FormHelper()
    helper.form_id = 'form'

# Form that allows user to cash out points
# TODO rewrite form
class CashOutPointsForm(forms.ModelForm):
    class Meta:
        model = User

        # layout where want fields to be, type in order you want it to appear
        fields = ('total_points', )

        # customize placeholders
        widgets = {
            'total_points':
            forms.NumberInput(attrs={
                'placeholder': 'Example: 10000',
            })
        }

        # customize form labels
        labels = {
            'total_points': 'Enter Amount of Points to Cash Out',
        }

    helper = FormHelper()
    helper.form_id = 'form'