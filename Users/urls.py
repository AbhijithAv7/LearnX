from django.urls import path
from .views import *

urlpatterns = [
    path('register/', role_select, name='role_select'),
    path('register/<str:role>/', register, name='register'),
    path('login/',user_login, name='login'),
    path('students/', view_students, name='view_students'),
    path('staff/', view_staff, name='view_staff'),
    path('instructor/',view_instructors,name='view_instructors'),
    path('user/update/<int:id>/',update_user, name='update_user'),
    path('user/delete/<int:id>/', delete_user, name='delete_user'),
    path('logout/',user_logout, name='logout'),
]