from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('instructor/dashboard/',instructor_dashboard, name='instructor_dashboard'),
    path('staff/dashboard/',staff_dashboard, name='staff_dashboard'),
    path('profile/', profile, name='profile'),
]