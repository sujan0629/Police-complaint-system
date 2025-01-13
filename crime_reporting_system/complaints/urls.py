from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('add_complaint/', views.add_complaint, name='add_complaint'),
    path('view_complaints/', views.view_complaints, name='view_complaints'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('people/', views.people, name='people'),
    path('user/profile/', views.user_profile_view, name='user_profile'),
    path('edit_user_profile/', views.edit_user_profile, name='edit_user_profile'),
    
    
    # Admin URLs
    path('rejected/', views.rejected_user_page, name='rejected_user_page'),
    path('register/', views.register_vehicle, name='register_vehicle'),
    path('search/', views.search_vehicle, name='search_vehicle'),
    path('vehicles/', views.list_of_registered_vehicles, name='list_of_registered_vehicles'),
    path('vehicles/<int:vehicle_id>/', views.view_vehicle_details, name='view_vehicle_details'),
    path('ip-track/', views.ip_track, name='ip_track'),
    path('map/', views.map, name='map_location'),
    path('verified-user/', views.verified_user_page, name='verified_user_page'),
     path('accept-user/<int:user_id>/', views.accept_user, name='accept_user'),
    path('reject-user/<int:user_id>/', views.reject_user, name='reject_user'),
    path('pending-verification/', views.pending_verification_view, name='pending_verification_page'),
    path('user_verification/', views.user_verification, name='user_verification'),
    path('admin_verification_page/', views.admin_verification_page, name='admin_verification_page'),
    path('verify_user/<int:user_id>/', views.verify_user, name='verify_user'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_profile/', views.admin_profile_view, name='admin_profile'),
     path('admin_profile_edit/', views.edit_admin_profile, name='edit_admin_profile'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_overview/', views.admin_overview, name='admin_overview'),
    path('pending_cases/', views.pending_cases, name='pending_cases'),
    path('completed_cases/', views.completed_cases, name='completed_cases'),
    path('update_status/<int:complaint_id>/', views.update_status, name='update_status'),
    path('admin_view_complaints/', views.admin_view_complaints, name='admin_view_complaints'),
    path('update_complaint_status/<int:complaint_id>/', views.update_complaint_status, name='update_complaint_status'),
]
