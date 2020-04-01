from django import forms
from django.contrib.auth.models import User
from .models import Complaint
from django.contrib.auth.forms import  AuthenticationForm
from django.forms.widgets import ClearableFileInput
from .models import UserProfile, AdminProfile
from .models import VehicleRegistration
# Update forms

class VehicleRegistrationForm(forms.ModelForm):
    class Meta:
        model = VehicleRegistration
        fields = '__all__'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture','user']  # Include fields as needed for user profile

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = [
            'name', 'caste', 'temp_address', 'perm_address', 'phone_number', 'profile_picture',
            'email', 'marital_status', 'post', 'citizenship_no', 'date_of_birth', 'age'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'full_name', 'date_of_birth', 'age', 'gender', 'phone_number', 'email', 'parent_name', 
            'citizenship_no', 'incident_type', 'incident_time', 'incident_date', 'incident_description', 
            'sound_recorder', 'evidence_1', 'evidence_2', 'evidence_3', 'evidence_4'
        ]
        widgets = {
            'incident_date': forms.DateInput(attrs={'type': 'date'}),
            'incident_time': forms.TimeInput(attrs={'type': 'time'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

# forms.py

# forms.py

from django import forms
from .models import UserVerification
from django.forms import ClearableFileInput

class UserVerificationForm(forms.ModelForm):
    class Meta:
        model = UserVerification
        fields = [
            'full_name',
            'date_of_birth',
            'district',
            'province',
            'city_name',
            'ward',
            'tole_name',
            'front_citizenship',
            'back_citizenship',
            'birth_certificate',
            'parent_name',
            'phone_number',
            'user_photo',  # Added user_photo field
        ]
    
    # Customize the form widgets
    full_name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Full Name'}))
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    district = forms.CharField(max_length=200, required=True)
    province = forms.CharField(max_length=200, required=True)
    city_name = forms.CharField(max_length=200, required=True)
    ward = forms.CharField(max_length=50, required=True)
    tole_name = forms.CharField(max_length=200, required=True)
    front_citizenship = forms.ImageField(required=False, widget=ClearableFileInput(attrs={'accept': 'image/*'}))
    back_citizenship = forms.ImageField(required=False, widget=ClearableFileInput(attrs={'accept': 'image/*'}))
    birth_certificate = forms.FileField(required=True)
    parent_name = forms.CharField(max_length=200, required=True)
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}))
    user_photo = forms.ImageField(required=False, widget=ClearableFileInput(attrs={'accept': 'image/*'}))  # Added user_photo field

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control'})
        self.fields['district'].widget.attrs.update({'class': 'form-control'})
        self.fields['province'].widget.attrs.update({'class': 'form-control'})
        self.fields['city_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['ward'].widget.attrs.update({'class': 'form-control'})
        self.fields['tole_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['front_citizenship'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['back_citizenship'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['birth_certificate'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['parent_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['user_photo'].widget.attrs.update({'class': 'form-control-file'})  # Added class for user_photo