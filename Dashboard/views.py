from django.shortcuts import render
# from .models import User, Course, Assignment
from Users.models import *
from Courses.models import *
from Academics.models import *


def home(request):
    return render(request, 'home.html')

def admin_dashboard(request):
    total_students = User.objects.filter(role='student').count()
    total_staff = User.objects.filter(role='staff').count()
    total_instructors = User.objects.filter(role='instructor').count()
    total_courses = Course.objects.count()
    total_instructor_allocations = InstructorAllocation.objects.count()
    total_staff_allocations = StaffAllocation.objects.count()
    total_exams = Exam.objects.count()
    total_assignments = Assignment.objects.count()
    total_materials = StudyMaterial.objects.count()
    # total_revenue = CoursePurchase.objects.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'total_students': total_students,
        'total_staff': total_staff,
        'total_instructors': total_instructors,
        'total_courses': total_courses,
        'total_instructor_allocations': total_instructor_allocations,
        'total_staff_allocations' : total_staff_allocations,
        'total_exams': total_exams,
        'total_assignments': total_assignments,
        'total_materials': total_materials,

        # 'total_assignments': total_assignments,
    }
    return render(request, 'admin_dashboard.html', context)

def student_dashboard(request):
    courses = Course.objects.all()

    context = {
        'courses': courses
    }

    return render(request, 'student_dashboard.html', context)

def instructor_dashboard(request):
    courses = Course.objects.all()

    context = {
        'courses': courses
    }

    return render(request, 'instructor_dashboard.html',context)

def staff_dashboard(request):
    courses = Course.objects.all()

    context = {
        'courses': courses
    }
    return render(request, 'staff_dashboard.html',context)

def profile(request):
    user = request.user

    if request.method == 'POST':
        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES.get('profile_image')

        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')

        user.save()

    if user.role == 'student':
        return render(request, 'student_profile.html', {'user': user})

    elif user.role == 'staff':
        return render(request, 'staff_profile.html', {'user': user})

    elif user.role == 'instructor':
        return render(request, 'instructor_profile.html', {'user': user})

    