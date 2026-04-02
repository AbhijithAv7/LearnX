from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [

    path('add-course/', add_course, name='add_course'),
    path('update-course/<int:id>/', update_course, name='update_course'),
    path('delete-course/<int:id>/', delete_course, name='delete_course'),    
    path('courses/', view_course, name='view_courses'),
    path('course_list/',course_list,name='course_list'),
    path('course/<int:id>/',course_detail, name='course_detail'),
    path('buy/<int:id>/',buy_course, name='buy_course'),
    path('allocate_instructor/',allocate_instructor,name='allocate_instructor'),
    path('allocate_staff',allocate_staff,name='allocate_staff'),
    path('Course_Management/',course_management,name='Course_Management'),
    path('course/<int:id>/', course_detail, name='course_detail'),
    path('enrolled_courses/',enrolled_courses,name='enrolled_courses'),
    path('enroll-list/', enroll_list, name='enroll_list'),
    path('approve/<int:id>/', approve_enrollment, name='approve_enrollment'),
    path('reject/<int:id>/', reject_enrollment, name='reject_enrollment'),
    path('staff/courses/', staff_courses, name='staff_courses'),
    path('instructor/courses',instructor_panel,name='instructor_courses'),
    path('create-batch/', create_batch, name='create_batch'),
    path('allocated-staff/', view_allocated_staff, name='view_allocated_staff'),
    path('staff-allocation/delete/<int:id>/',delete_staff_allocation, name='delete_staff_allocation'),
    path('staff-allocation/update/<int:id>/', update_staff_allocation, name='update_staff_allocation'),
    path('allocated-instructor/', view_allocated_instructor, name='view_allocated_instructor'),
    path('instructor-allocation/delete/<int:id>/',delete_instructor_allocation, name='delete_instructor_allocation'),
    path('instructor-allocation/update/<int:id>/',update_instructor_allocation, name='update_instructor_allocation'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)