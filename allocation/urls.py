from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about_us, name='about'),
    path('contact/', views.contact_us, name='contact'),

    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('authority_dashboard/', views.authority_dashboard, name='authority_dashboard'),

    path('application/approve/<int:app_id>/', views.approve_application, name='approve_application'),
    path('application/reject/<int:app_id>/', views.reject_application, name='reject_application'),

    path('student/apply-room/', views.student_apply_room, name='student_apply_room'),

    # allocation/urls.py
    path('student/profile/', views.profile_update, name='profile_update'),

    path('available-rooms/', views.available_rooms, name='available_rooms'),

    path('application/approve/<int:app_id>/', views.approve_application, name='approve_application'),
    path('application/reject/<int:app_id>/', views.reject_application, name='reject_application'),


]