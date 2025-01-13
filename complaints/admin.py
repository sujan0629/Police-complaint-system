from django.contrib import admin
from .models import Complaint, AdminProfile, UserProfile

admin.site.register(Complaint)
admin.site.register(AdminProfile)
admin.site.register(UserProfile)

