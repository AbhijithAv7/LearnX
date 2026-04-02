from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import *
from Users.models import *
from Academics.models import *

def add_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        price = request.POST.get('price')
        image = request.FILES.get('image')   

        Course.objects.create(
            title=title,
            description=description,
            duration=duration,
            price=price,
            image=image
        )
        return redirect('view_courses')

    return render(request, 'add_course.html')

def view_course(request):
    courses = Course.objects.all()
    return render(request, 'view_course.html', {'courses': courses})

def course_list(request):
    if request.user.role not in ['student', 'staff', 'instructor']:
        return redirect('home')

    courses = Course.objects.all()

    purchased_courses = CoursePurchase.objects.filter(
        user=request.user
    ).values_list('course_id', flat=True)

    return render(request, 'courses.html', {
        'courses': courses,
        'purchased_courses': purchased_courses
    })

def staff_courses(request):

    allocated = StaffAllocation.objects.filter(staff=request.user)
    courses = Course.objects.filter(id__in=allocated.values_list('course_id', flat=True))

    return render(request, 'staff_courses.html', {
        'courses': courses
    })
def instructor_panel(request):
    tab = request.GET.get('tab', 'courses')
    subtab = request.GET.get('subtab', 'lesson')

    courses = Course.objects.all()

    
    my_courses = Course.objects.filter(
        instructorallocation__instructor=request.user
    )

    selected_course_id = request.GET.get('course_id')
    course = None

    lessons = exams = assignments = materials = None

    if selected_course_id:
        course = get_object_or_404(Course, id=selected_course_id)

        lessons = Lesson.objects.filter(course=course)
        exams = Exam.objects.filter(course=course)
        assignments = Assignment.objects.filter(course=course)
        materials = StudyMaterial.objects.filter(course=course)

    return render(request, 'instructor_courses.html', {
        'tab': tab,
        'subtab': subtab,
        'courses': courses,
        'my_courses': my_courses,
        'course': course,
        'lessons': lessons,
        'exams': exams,
        'assignments': assignments,
        'materials': materials,
    })

def update_course(request, id):
    course = get_object_or_404(Course, id=id)

    if request.method == 'POST':
        course.title = request.POST.get('title')
        course.description = request.POST.get('description')
        course.duration = request.POST.get('duration')
        course.save()

        return redirect('course_list')

    return render(request, 'update_course.html', {'course': course})

def delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    course.delete()

    return redirect('view_courses')

def enroll_list(request):
    tab = request.GET.get('type', 'pending')

    if tab == 'approved':
        enrollments = CoursePurchase.objects.filter(status='approved')
    else:
        enrollments = CoursePurchase.objects.filter(status='pending')

    return render(request, 'enroll_list.html', {
        'enrollments': enrollments,
        'tab': tab
    })

def approve_enrollment(request, id):
    enrollment = get_object_or_404(CoursePurchase, id=id)
    enrollment.status = 'approved'
    enrollment.save()
    return redirect('enroll_list')


def reject_enrollment(request, id):
    enrollment = get_object_or_404(CoursePurchase, id=id)
    enrollment.status = 'rejected'
    enrollment.save()
    return redirect('enroll_list')

def allocate_instructor(request):
    instructors = User.objects.filter(role='instructor')  
    courses = Course.objects.all()
    batches = Batch.objects.all() 

    if request.method == 'POST':
        instructor_id = request.POST['instructor']
        course_id = request.POST['course']
        batch_name = request.POST['batch']

        InstructorAllocation.objects.create(
            instructor_id=instructor_id,
            course_id=course_id,
            batch=batch_name
        )

        return redirect('Course_Management')

    return render(request, 'allocate_instructor.html', {
        'instructors': instructors,
        'courses': courses,
        'batches': batches
    })

def view_allocated_instructor(request):
    allocations = InstructorAllocation.objects.all()

    return render(request, 'view_allocated_instructor.html', {
        'allocations': allocations
    })

def delete_instructor_allocation(request, id):
    alloc = get_object_or_404(InstructorAllocation, id=id)
    alloc.delete()
    return redirect('view_instructor_allocations')


def update_instructor_allocation(request, id):
    alloc = get_object_or_404(InstructorAllocation, id=id)

    if request.method == "POST":
        alloc.instructor_id = request.POST.get('instructor')
        alloc.course_id = request.POST.get('course')
        alloc.batch_id = request.POST.get('batch')
        alloc.save()
        
        return redirect('view_instructor_allocations')

    instructors = User.objects.filter(role='instructor')
    courses = Course.objects.all()
    batches = Batch.objects.all()

    return render(request, 'update_instructor_allocation.html', {
        'alloc': alloc,
        'instructors': instructors,
        'courses': courses,
        'batches': batches
    })

def allocate_staff(request):
    staff_members = User.objects.filter(role='staff')  
    courses = Course.objects.all()
    batches = Batch.objects.all() 

    if request.method == 'POST':
        staff_id = request.POST.get('staff')
        course_id = request.POST.get('course')
        batch_name = request.POST.get('batch')

        staff = User.objects.get(id=staff_id)
        course = Course.objects.get(id=course_id)

        
        StaffAllocation.objects.create(
            staff=staff,
            course=course,
            batch=batch_name
        )
        return redirect('Course_Management')  

    return render(request, 'allocate_staff.html', {
        'staff_members': staff_members,
        'courses': courses,
        'batches': batches
    })

def view_allocated_staff(request):
    allocations = StaffAllocation.objects.all()

    return render(request, 'view_allocated_staff.html', {
        'allocations': allocations
    })


def delete_staff_allocation(request, id):
    alloc = get_object_or_404(StaffAllocation, id=id)
    alloc.delete()
    return redirect('view_staff_allocations')


def update_staff_allocation(request, id):
    alloc = get_object_or_404(StaffAllocation, id=id)

    if request.method == "POST":
        alloc.staff_id = request.POST.get('staff')
        alloc.course_id = request.POST.get('course')
        alloc.batch_id = request.POST.get('batch')
        alloc.save()
        return redirect('view_staff_allocations')

    staffs = User.objects.filter(role='staff')
    courses = Course.objects.all()
    batches = Batch.objects.all()

    return render(request, 'update_staff_allocation.html', {
        'alloc': alloc,
        'staffs': staffs,
        'courses': courses,
        'batches': batches
    })

def course_management(request):
    return render(request,'Course_Management.html')


def course_detail(request, id):
    course = get_object_or_404(Course, id=id)

    lessons = Lesson.objects.filter(course=course)
    assignments = Assignment.objects.filter(course=course)
    materials = StudyMaterial.objects.filter(course=course)

    purchase = None
    is_allowed = False

    selected_lesson = None
    lesson_id = request.GET.get('lesson_id')

    if lesson_id:
        selected_lesson = Lesson.objects.filter(id=lesson_id, course=course).first()
    elif lessons.exists():
        selected_lesson = lessons.first()

    if request.user.is_authenticated:

        # ✅ Instructor check
        is_instructor = InstructorAllocation.objects.filter(
            course=course,
            instructor=request.user
        ).exists()

        # ✅ NEW: Staff check
        is_staff_allocated = StaffAllocation.objects.filter(
            course=course,
            staff=request.user
        ).exists()

        if is_instructor or is_staff_allocated:
            is_allowed = True

        else:
            # ✅ Student purchase check
            purchase = CoursePurchase.objects.filter(
                user=request.user,
                course=course
            ).first()

            is_allowed = purchase and purchase.status == 'approved'

        # Exams
        attended_exam_ids = StudentExam.objects.filter(
            student=request.user,
            submitted=True
        ).values_list('exam_id', flat=True)

        exams = Exam.objects.filter(course=course).exclude(id__in=attended_exam_ids)

    else:
        exams = Exam.objects.filter(course=course)

    return render(request, 'course_detail.html', {
        'course': course,
        'lessons': lessons,
        'exams': exams,
        'assignments': assignments,
        'materials': materials,
        'is_allowed': is_allowed,
        'purchase': purchase,
        'selected_lesson': selected_lesson
    })

def buy_course(request, id):
    course = get_object_or_404(Course, id=id)

    purchase, created = CoursePurchase.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={'status': 'pending'}
    )

    if created:
        messages.success(request, "Enrollment request sent successfully.")
    else:
        if purchase.status == 'pending':
            messages.warning(request, "You have already requested this course.")
        elif purchase.status == 'approved':
            messages.info(request, "You are already enrolled in this course.")
        elif purchase.status == 'rejected':

            purchase.status = 'pending'
            purchase.save()
            messages.success(request, "Request resubmitted.")

    return redirect('course_detail', id=id)

def create_batch(request):
    courses = Course.objects.all()

    if request.method == 'POST':
        course_id = request.POST.get('course')
        batch_name = request.POST.get('batch_name')

        Batch.objects.create(
            course_id=course_id,
            name=batch_name
        )

        return redirect('create_batch')

    return render(request, 'create_batch.html', {
        'courses': courses
    })

def enrolled_courses(request):
    return render(request,'enrolled_courses.html')