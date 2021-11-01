from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import PasswordInput
from .models import User, School
from crispy_forms.helper import FormHelper
from django.contrib.auth import get_user_model

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
class PurchasePointsForm(forms.Form):
    def __init__(self, *args,**kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args,**kwargs)

        self.fields ['purchased_points'] = forms.IntegerField(label = 'Enter amount to purchase (points)')
        self.fields ['purchased_points'].initial = 0
        self.fields ['purchased_points'].widget.attrs['placeholder'] = 'Number of points'

    def clean_purchased_points (self): #validate purchased points field
        purchased_points = self.cleaned_data['purchased_points']
        if (purchased_points == None or purchased_points <= 0):
            self.add_error ('purchased_points', 'Please enter a positive value.')
        return purchased_points

    def save(self):
        self.user.total_points += self.cleaned_data['purchased_points'] #save if positive
        self.user.save()

# Form that allows user to cash out points
class CashOutPointsForm(forms.Form):
    def __init__(self, *args,**kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args,**kwargs)

        self.fields ['cashed_points'] = forms.FloatField(label = 'Enter amount to cash out (points)')
        self.fields ['cashed_points'].initial = 0
        self.fields ['cashed_points'].widget.attrs['placeholder'] = 'Number of points'

    def clean_cashed_points (self): #validate cashed points field
        cashed_points = self.cleaned_data['cashed_points']
        if (cashed_points == None or cashed_points <= 0):
            self.add_error ('cashed_points', 'Please enter a positive value.')
        elif (cashed_points > self.user.total_points): #if user tries to cash out more points than point balance
            self.add_error ('cashed_points', 'Please enter a value less than or equal to your points balance.')
        return cashed_points

    def save(self):
        self.user.total_points -= self.cleaned_data['cashed_points']
        self.user.save()

# Form that allows user to transfer points from one person to another
class TransferPointsForm(forms.Form):

    def __init__(self, *args,**kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args,**kwargs)
        self.fields ['tutors'] = forms.ModelChoiceField(label = 'Select Tutor', queryset = get_user_model().objects.all().filter(is_tutor = True,school = self.user.school).exclude (pk = self.user.id))
        self.fields ['amount_to_transfer'] = forms.IntegerField(label = 'Enter the amount to transfer (points)')
        self.fields ['amount_to_transfer'].initial = 0
        self.fields ['amount_to_transfer'].widget.attrs['placeholder'] = 'Number of points'
        self.error_css_class = 'error'

    def clean_amount_to_transfer (self): #validate amount to transfer field
        amount_to_transfer = self.cleaned_data['amount_to_transfer']
        if (amount_to_transfer == None or amount_to_transfer <= 0): #if they didnt enter a positive number
            self.add_error ('amount_to_transfer', 'Please enter a positive value.')
        elif (amount_to_transfer > self.user.total_points): #if user tries to transfer more points than point balance
            self.add_error ('amount_to_transfer', "Please enter a value less than or equal to your current points balance.")
        return amount_to_transfer

    def clean_tutors(self): #validate tutors field
        tutor = self.cleaned_data['tutors']
        if (tutor == None):
            self.add_error ('tutors', "Please choose a tutor")
        return tutor

    def save(self):
        amount_to_transfer = self.cleaned_data['amount_to_transfer']
        tutor = self.cleaned_data['tutors']
        self.user.total_points -= amount_to_transfer
        self.user.save()
        tutor.total_points += amount_to_transfer
        tutor.save()
