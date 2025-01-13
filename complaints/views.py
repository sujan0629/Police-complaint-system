from django.shortcuts import render, redirect, get_object_or_404
from .forms import ComplaintForm, UserSignupForm
from .models import Complaint,  AdminProfile
from django.contrib.auth import login, authenticate
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserSignupForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q
from datetime import date, timedelta
from django.db.models import Count
from datetime import datetime
import calendar
from .models import UserProfile, AdminProfile
from .forms import UserProfileForm, AdminProfileForm
from django.shortcuts import render, redirect
from .models import UserVerification
from django.contrib.admin.views.decorators import staff_member_required
from .forms import UserVerificationForm
from .models import UserVerification
import requests
from django.http import JsonResponse
from .models import VehicleRegistration
from .forms import VehicleRegistrationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import CrimeReport
import time

# View to render the page for registering crime through AI
def register_crime(request):
    return render(request, 'register_crime.html')

# View to handle the case registration
def voice_registered_case(request):
    if request.method == 'POST':
        crime_details = request.POST
        crime_type = crime_details.get('crime_type')
        incident_time = crime_details.get('incident_time')
        incident_date = crime_details.get('incident_date')
        description = crime_details.get('description')

        # Save the crime report to the database
        crime_report = CrimeReport.objects.create(
            crime_type=crime_type,
            incident_date=incident_date,
            incident_time=incident_time,
            description=description,
            created_at=time.ctime()
        )

        return render(request, 'voice_registered_case.html', {'crime_report': crime_report})

    return redirect('home')  # Redirect to homepage if it's not a POST request


def home(request):
    return render(request, 'home.html')

def list_of_registered_vehicles(request):
    vehicles = VehicleRegistration.objects.all()
    return render(request, 'list_of_registered_vehicles.html', {'vehicles': vehicles})

def view_vehicle_details(request, vehicle_id):
    vehicle = get_object_or_404(VehicleRegistration, id=vehicle_id)
    return render(request, 'vehicle_details.html', {'vehicle': vehicle})

def register_vehicle(request):
    if request.method == "POST":
        form = VehicleRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')
    else:
        form = VehicleRegistrationForm()
    return render(request, 'register_vehicle.html', {'form': form})

def search_vehicle(request):
    if request.method == "POST":
        vehicle_no = request.POST.get('vehicle_no')
        vehicle = get_object_or_404(VehicleRegistration, vehicle_no=vehicle_no)
        return render(request, 'vehicle_info.html', {'vehicle': vehicle})
    return render(request, 'search_vehicle.html')




# Function to render the map with the form for longitude and latitude
def map(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        # You can use an external service or API to convert these coordinates to a location
        # Here, we'll just return the coordinates as part of the response
        return render(request, 'map.html', {
            'latitude': latitude,
            'longitude': longitude,
        })
    return render(request, 'map.html')

def ip_track(request):
    latitude = None
    longitude = None

    if request.method == 'POST':
        ip_address = request.POST.get('ip_address')
        
        # Use an external API to get location based on IP address
        url = f'http://ip-api.com/json/{ip_address}'
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'fail':
            message = "Invalid IP address"
        else:
            latitude = data.get('lat')
            longitude = data.get('lon')
            message = f"Location of IP {ip_address} is Latitude: {latitude}, Longitude: {longitude}"

        return render(request, 'ip_track.html', {'latitude': latitude, 'longitude': longitude, 'message': message, 'ip_address': ip_address})

    return render(request, 'ip_track.html')





def edit_user_profile(request):
    # Get the current user’s verification data
    user_verification = request.user.userverification

    if request.method == 'POST':
        form = UserVerificationForm(request.POST, request.FILES, instance=user_verification)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  # Redirect to user profile page after saving
    else:
        form = UserVerificationForm(instance=user_verification)

    return render(request, 'edit_user_profile.html', {'form': form})

def rejected_user_page(request):
    # Logic for the rejected user page
    return render(request, 'rejected_user.html')

@login_required
def verified_user_page(request):
    # Get the list of verified users (approved status)
    verified_users = UserVerification.objects.filter(is_verified=True)

    # Return the template showing the verified users
    return render(request, 'verified_user_page.html', {'verified_users': verified_users})


def accept_user(request, user_id):
    user = UserVerification.objects.get(id=user_id)
    user.is_verified = True  # Mark the user as verified
    user.save()  # Save the changes to the database
    return redirect('verified_user_page')  # Redirect to verified user page

def reject_user(request, user_id):
    user = UserVerification.objects.get(id=user_id)
    user.status = 'rejected'  # Change the status to 'rejected'
    user.save()
    return redirect('admin_verification_page')  # Redirect back to the admin verification page

def pending_verification_view(request):
    # Fetch all users whose verification status is 'pending'
    pending_users = UserVerification.objects.filter(status='pending')

    # Pass the list of pending users to the template
    return render(request, 'pending_verification.html', {'pending_users': pending_users})

def user_verification(request):
    # If the user has already submitted their verification form, we redirect them
    if UserVerification.objects.filter(user=request.user).exists():
        return redirect('home')  # Redirect to user dashboard or any page you want

    if request.method == 'POST':
        form = UserVerificationForm(request.POST, request.FILES)  # Pass request.FILES to handle file uploads
        if form.is_valid():
            # Save the form data to a new UserVerification model instance
            user_verification = UserVerification(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                district=form.cleaned_data['district'],
                province=form.cleaned_data['province'],
                city_name=form.cleaned_data['city_name'],
                ward=form.cleaned_data['ward'],
                tole_name=form.cleaned_data['tole_name'],
                front_citizenship=form.cleaned_data.get('front_citizenship'),
                back_citizenship=form.cleaned_data.get('back_citizenship'),
                birth_certificate=form.cleaned_data['birth_certificate'],
                parent_name=form.cleaned_data['parent_name'],
                phone_number=form.cleaned_data['phone_number'],
                user_photo=form.cleaned_data.get('user_photo'),  # Save the user_photo field
                is_verified=False  # Initially, the user is not verified
            )
            user_verification.save()

            return redirect('pending_verification_page')  # Redirect to admin verification page
    else:
        form = UserVerificationForm()

    return render(request, 'user_verification.html', {'form': form})

@staff_member_required
def admin_verification_page(request):
    # Get all unverified users (where is_verified is False)
    unverified_users = UserVerification.objects.filter(is_verified=False)

    return render(request, 'admin_verification_page.html', {'unverified_users': unverified_users})


@staff_member_required
def verify_user(request, user_id):
    user_verification = UserVerification.objects.get(id=user_id)
    if request.method == 'POST':
        # Mark the user as verified
        user_verification.is_verified = True
        user_verification.save()

        # Redirect to admin verification page
        return redirect('admin_verification_page')

    return render(request, 'verify_user.html', {'user_verification': user_verification})




def edit_admin_profile(request):
    admin_profile = AdminProfile.objects.get(user=request.user)  # Get the admin profile of the logged-in user

    if request.method == 'POST':
        form = AdminProfileForm(request.POST, request.FILES, instance=admin_profile)
        if form.is_valid():
            form.save()
            return redirect('admin_profile')  # Redirect to the profile page after editing
    else:
        form = AdminProfileForm(instance=admin_profile)
    
    return render(request, 'edit_admin_profile.html', {'form': form})




@login_required
def user_profile_view(request):
    # Get the logged-in user
    user = request.user

    # Retrieve the UserVerification model for the logged-in user
    try:
        user_verification = user.userverification
    except UserVerification.DoesNotExist:
        user_verification = None  # If the user doesn't have a verification entry yet

    return render(request, 'user_profile.html', {
        'user': user,
        'user_verification': user_verification,
    })
@login_required
def admin_profile_view(request):
    # Fetch the AdminProfile related to the currently logged-in user
    admin_profile = AdminProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = AdminProfileForm(request.POST, request.FILES, instance=admin_profile)
        if form.is_valid():
            form.save()
            return redirect('admin_profile')  # Redirect after saving the changes
    else:
        form = AdminProfileForm(instance=admin_profile)  # Pre-fill the form with existing profile data

    # Return the admin profile page with the form
    return render(request, 'admin_profile.html', {'form': form, 'admin_profile': admin_profile})

@login_required
def admin_overview(request):
    # Real-time chart data
    today = datetime.today().date()
    yesterday = today - timedelta(days=1)
    complaints_today = Complaint.objects.filter(incident_date=today).count()
    complaints_yesterday = Complaint.objects.filter(incident_date=yesterday).count()

    # Pie chart: Incident Type Distribution
    incident_types = Complaint.objects.values('incident_type').annotate(total=Count('id'))

    # Bar chart: Complaints over the current year and previous years
    current_year = today.year
    past_years = [current_year - 1, current_year - 2]
    complaints_per_year = Complaint.objects.filter(incident_date__year__in=[current_year, *past_years]) \
                                            .values('incident_date__year') \
                                            .annotate(total=Count('id'))

    # Prepare data for the charts
    context = {
        'complaints_today': complaints_today,
        'complaints_yesterday': complaints_yesterday,
        'incident_types': incident_types,
        'complaints_per_year': complaints_per_year,
        'today': today,
        'current_year': current_year,
        'past_years': past_years
    }
    return render(request, 'overview.html', context)

  


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('/admin_dashboard/')  # Redirect to admin dashboard or another custom page
        else:
            messages.error(request, 'Invalid credentials or unauthorized access.')
    return render(request, 'admin_custom_login.html')





def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            # Check if the user is verified before logging them in
            if hasattr(user, 'userverification') and user.userverification.is_verified:
                login(request, user)
                return redirect('people')  # Redirect to homepage or desired page after login
            else:
                # Show a message if the user is not verified
                messages.error(request, "Your account is not verified yet. Please wait for admin verification.")
                return redirect('login')  # Optionally, redirect back to the login page or a verification page
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout



def update_complaint_status(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    if complaint.status == 'pending':
        complaint.status = 'completed'
    else:
        complaint.status = 'pending'
    
    complaint.save()
    return redirect('admin_view_complaints')

def admin_view_complaints(request):
    complaints = Complaint.objects.all()  # Fetch all complaints
    return render(request, 'admin_view_complaints.html', {'complaints': complaints})


@login_required
def full_case_view(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    return render(request, 'complaints/full_case_view.html', {'complaint': complaint})

# User Views
def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_verification')
    else:
        form = UserSignupForm()
    return render(request, 'signup.html', {'form': form})

def home(request):
    return render(request, 'home.html')

@login_required
def people(request):
       # Check if the user's account is approved
    user_verification = UserVerification.objects.filter(user=request.user).first()

    if not user_verification or user_verification.status == False:
        return redirect('rejected_user_page')

    # If verified, show the user profile
    return render(request, 'user.html', {'user': request.user})


@login_required
def add_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new complaint instance but don't save it yet
            complaint = form.save(commit=False)

            # Assign the logged-in user to the complaint
            complaint.user = request.user

            # Capture the user's IP address
            complaint.ip_address = request.META.get('REMOTE_ADDR')

            # Save the complaint to the database
            complaint.save()

            # Redirect to a view that lists complaints (you can define this view separately)
            return redirect('view_complaints')  # Assuming 'view_complaints' is the URL name for listing complaints
    else:
        form = ComplaintForm()  # If it's a GET request, just create an empty form

    # Render the form on the page (add_complaint.html)
    return render(request, 'add_complaint.html', {'form': form})

@login_required
def view_complaints(request):
    complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'view_complaints.html', {'complaints': complaints})

# Admin Views
@login_required
def admin_dashboard(request):
      # 1. Count pending and completed cases
    pending_count = Complaint.objects.filter(status='pending').count()
    completed_count = Complaint.objects.filter(status='completed').count()

    # 2. Count today’s cases
    today = timezone.now().date()
    today_cases = Complaint.objects.filter(created_at__date=today).count()

    # 3. Calculate the percentage increase in cases
    yesterday = today - timedelta(days=1)
    yesterday_cases = Complaint.objects.filter(created_at__date=yesterday).count()
    if yesterday_cases > 0:
        case_increase_percentage = ((today_cases - yesterday_cases) / yesterday_cases) * 100
    else:
        case_increase_percentage = 100 if today_cases > 0 else 0
     # Cases for this month
    daily_cases_this_month = []
    days_in_month = []
    for i in range(1, today.day + 1):
        day = today.replace(day=i)
        days_in_month.append(day.strftime('%Y-%m-%d'))
        daily_cases_this_month.append(Complaint.objects.filter(incident_date=day).count())

    admin_profile = AdminProfile.objects.get(user=request.user)
    context = {
        'pending_count': pending_count,
        'completed_count': completed_count,
        'today_cases': today_cases,
        'case_increase_percentage': case_increase_percentage,
        'days_in_month': days_in_month,
        'daily_cases_this_month': daily_cases_this_month,
        'yesterdays_cases': yesterday_cases,
        'admin_name': admin_profile.name,  # Admin's name
        'admin_photo': admin_profile.profile_picture.url if admin_profile.profile_picture else None  # Admin's photo

    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def pending_cases(request):
    complaints = Complaint.objects.filter(status='pending')
    return render(request, 'pending_cases.html', {'complaints': complaints})

@login_required
def completed_cases(request):
    complaints = Complaint.objects.filter(status='completed')
    return render(request, 'completed_cases.html', {'complaints': complaints})

@login_required
def update_status(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    if request.method == 'POST':
        complaint.status = request.POST.get('status')
        complaint.save()
        return redirect('pending_cases')
    return render(request, 'update_status.html', {'complaint': complaint})
