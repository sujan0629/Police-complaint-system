# complaints/models.py
from django.db import models
from django.contrib.auth.models import User
from django.forms.widgets import ClearableFileInput
from django.db import models

class CrimeReport(models.Model):
    crime_type = models.CharField(max_length=255)
    incident_date = models.DateField()
    incident_time = models.TimeField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Crime Report: {self.crime_type} on {self.incident_date}"



class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    
    # Existing fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # New fields
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    parent_name = models.CharField(max_length=255)
    citizenship_no = models.CharField(max_length=50)
    incident_type = models.CharField(max_length=100)
    incident_time = models.TimeField()
    incident_date = models.DateField()
    incident_description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    sound_recorder = models.FileField(upload_to='sound_recordings/', blank=True, null=True)
    evidence_1 =  models.ImageField(upload_to='evidence/', blank=True, null=True)
    evidence_2 =  models.ImageField(upload_to='evidence/', blank=True, null=True)
    evidence_3 =  models.ImageField(upload_to='evidence/', blank=True, null=True)
    evidence_4 =  models.ImageField(upload_to='evidence/', blank=True, null=True)

    def __str__(self):
        return self.title
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    # Add any additional fields specific to user sign-up info if needed

    def __str__(self):
        return f"{self.user.username}'s Profile"
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='admin_pictures/', blank=True, null=True)
    name = models.CharField(max_length=100)
    caste = models.CharField(max_length=50)
    temp_address = models.TextField("Temporary Address")
    perm_address = models.TextField("Permanent Address")
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    
    MARITAL_STATUS_CHOICES = [
        ('Married', 'Married'),
        ('Single', 'Single')
    ]
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    post = models.CharField(max_length=50)
    citizenship_no = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    age = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}'s Admin Profile"
class UserVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    district = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    city_name = models.CharField(max_length=100)
    ward = models.CharField(max_length=10)
    tole_name = models.CharField(max_length=100)
    front_citizenship = models.ImageField(upload_to='citizenship/', null=True, blank=True)
    back_citizenship = models.ImageField(upload_to='citizenship/', null=True, blank=True)
    birth_certificate = models.ImageField(upload_to='birth_certificates/', null=True, blank=True)
    parent_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)  # Set to False initially
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    user_photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)  # Added user photo field
    
    def __str__(self):
        return self.full_name
    
class VehicleRegistration(models.Model):
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    gender_choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender = models.CharField(max_length=1, choices=gender_choices)
    
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    citizenship_no = models.CharField(max_length=50)
    licence_no = models.CharField(max_length=50)
    bought_from = models.CharField(max_length=255)
    engine_no = models.CharField(max_length=50)
    vehicle_no = models.CharField(max_length=50)  # Save Nepali numbers here

    transpo_type_choices = [('Two-Wheeler', 'Two-Wheeler'), ('Four-Wheeler', 'Four-Wheeler'), ('Heavy Vehicle', 'Heavy Vehicle')]
    transpo_type = models.CharField(max_length=20, choices=transpo_type_choices)
    bought_date = models.DateField()

    district = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    city_name = models.CharField(max_length=100)
    ward = models.IntegerField()
    tole_name = models.CharField(max_length=100)

    front_citizenship = models.ImageField(upload_to='documents/citizenship/front/')
    back_citizenship = models.ImageField(upload_to='documents/citizenship/back/')
    user_photo = models.ImageField(upload_to='documents/user_photos/')
    vehicle_papers = models.FileField(upload_to='documents/vehicle_papers/', blank=True, null=True)
    
    vehicle_front_photo = models.ImageField(upload_to='vehicles/photos/front/')
    vehicle_back_photo = models.ImageField(upload_to='vehicles/photos/back/')
    vehicle_left_photo = models.ImageField(upload_to='vehicles/photos/left/')
    vehicle_right_photo = models.ImageField(upload_to='vehicles/photos/right/')

    def __str__(self):
        return self.vehicle_no
