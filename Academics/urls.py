from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('student/attendance/', student_attendance, name='student_attendance'),
    path('mark-attendance/<int:lesson_id>/',mark_attendance, name='mark_attendance'),
    path('student_marks',student_marks,name='student_marks'),
    path('attendance-log/', attendance_log, name='attendance_log'),
    path('add-exam/<int:course_id>/',add_exam, name='add_exam'),
    path('exam/<int:exam_id>/add-question/',add_question, name='add_question'),
    path('exam/<int:exam_id>/',attend_exam, name='attend_exam'),
    path('exam-result/<int:exam_id>/',exam_result, name='exam_result'),
    path('add-assignment/<int:course_id>/',add_assignment, name='add_assignment'),
    path('assignment/<int:assignment_id>/',assignment_detail, name='assignment_detail'),
    path('assignment-submissions/<int:assignment_id>/',view_assignment_submissions, name='view_assignment_submissions'),
    path('instructor/assignments/',instructor_assignments, name='instructor_assignments'),
    path('evaluate/<int:submission_id>/', evaluate_submission, name='evaluate_submission'),
    path('add-material/<int:course_id>/',add_material, name='add_material'),
    path('materials/<int:course_id>/', view_materials, name='view_materials'),
    path('lesson/add/<int:course_id>/',add_lesson, name='add_lesson'),
    path('exam/<int:exam_id>/questions/',view_questions, name='view_questions'),
    path('question/edit/<int:id>/',edit_question, name='edit_question'),
    path('course/<int:course_id>/lessons/',view_lessons, name='view_lessons'),
    path('mark_watched/<int:lesson_id>/', mark_watched),
    path('course/<int:course_id>/progress/',course_progress, name='course_progress'),
    path('manage-content/',manage_content, name='manage_content'),
    path('delete-lesson/<int:id>/',delete_lesson, name='delete_lesson'),
    path('delete-exam/<int:id>/',delete_exam, name='delete_exam'),
    path('delete-assignment/<int:id>/',delete_assignment, name='delete_assignment'),
    path('delete-material/<int:id>/',delete_material, name='delete_material'),
    path('enrolled-courses/',enrolled_courses, name='enrolled_courses'),
    path('admin-view-exams/', admin_view_exams, name='admin_view_exams'),
    path('admin-view-assignments/', admin_view_assignments, name='admin_view_assignments'),
    path('admin-view-materials/',admin_view_materials, name='admin_view_materials'),
    path('contact/',contact_view, name='contact'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)