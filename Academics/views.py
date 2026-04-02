from django.shortcuts import render, redirect, get_object_or_404
from .models import*
from Courses.models import *
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from django.contrib import messages

def student_attendance(request):
    attendances = Attendance.objects.filter(student=request.user)

    return render(request, 'student_attendance.html', {
        'attendances': attendances
    })

def student_marks(request):
    submissions = AssignmentSubmission.objects.filter(student=request.user)

    return render(request, 'student_marks.html', {
        'submissions': submissions
    })

def attendance_log(request):
    staff = request.user

    allocations = StaffAllocation.objects.filter(staff=staff)

    data = []

    for alloc in allocations:
        course = alloc.course
        batch = alloc.batch

        # students in this batch
        students = CoursePurchase.objects.filter(
            course=course
        ).select_related('user')

        for s in students:
            student = s.user

            # check if attended ANY lesson
            attended = Attendance.objects.filter(
                student=student,
                lesson__course=course,
                watched=True
            ).exists()

            data.append({
                'student': student.username,
                'status': 'Present' if attended else 'Not Watched'
            })

    return render(request, 'attendance_log.html', {
        'data': data
    })


def add_exam(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        title = request.POST.get('title')

        
        exam = Exam.objects.create(course=course, title=title)

        return redirect('add_question', exam_id=exam.id)

    return render(request, 'add_exam.html', {'course': course})

def add_question(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == 'POST':

        if 'add_more' in request.POST:
            Question.objects.create(
                exam=exam,
                question_text=request.POST.get('question'),
                option1=request.POST.get('o1'),
                option2=request.POST.get('o2'),
                option3=request.POST.get('o3'),
                option4=request.POST.get('o4'),
                correct_option=int(request.POST.get('correct'))
            )

            return redirect('add_question', exam_id=exam.id)


        if 'finish' in request.POST:
            return redirect(
                f'/Courses/instructor/courses?tab=academics&course_id={exam.course.id}&subtab=exam'
            )

    questions = Question.objects.filter(exam=exam)

    return render(request, 'add_question.html', {
        'exam': exam,
        'questions': questions
    })

def view_questions(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = Question.objects.filter(exam=exam)

    return render(request, 'view_questions.html', {
        'exam': exam,
        'questions': questions
    })

def edit_question(request, id):
    question = get_object_or_404(Question, id=id)
    exam = question.exam

    if request.method == 'POST':
        # ✅ update exam title
        exam.title = request.POST.get('exam_title')
        exam.save()

        # ✅ update question
        question.question_text = request.POST.get('question')
        question.option1 = request.POST.get('o1')
        question.option2 = request.POST.get('o2')
        question.option3 = request.POST.get('o3')
        question.option4 = request.POST.get('o4')
        question.correct_option = request.POST.get('correct')
        question.save()

        return redirect('view_questions', exam_id=exam.id)

    return render(request, 'edit_question.html', {
        'q': question,
        'exam': exam
    })

# def delete_question(request, id):
#     question = get_object_or_404(Question, id=id)
#     exam_id = question.exam.id

#     question.delete()

#     return redirect('view_questions', exam_id=exam_id)


def attend_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = Question.objects.filter(exam=exam)

    student_exam, created = StudentExam.objects.get_or_create(
        student=request.user,
        exam=exam
    )

    if student_exam.submitted:
        return redirect('exam_result', exam_id=exam.id)

    if request.method == 'POST':
        score = 0
        answers = []

        
        StudentAnswer.objects.filter(student_exam=student_exam).delete()

        for q in questions:
            selected = request.POST.get(f'question_{q.id}')

            
            if selected is None:
                continue

            selected = int(selected)

            StudentAnswer.objects.create(
                student_exam=student_exam,
                question=q,
                selected_option=selected
            )

            is_correct = selected == q.correct_option

            if is_correct:
                score += 1

            answers.append({
                'question': q,
                'selected': selected,
                'correct': q.correct_option,
                'is_correct': is_correct
            })


        student_exam.score = score
        student_exam.submitted = True   
        student_exam.save()

        return render(request, 'exam_result.html', {
            'exam': exam,
            'answers': answers,
            'score': score,
            'total': questions.count()
        })

    return render(request, 'attend_exam.html', {
        'exam': exam,
        'questions': questions
    })

def exam_result(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    # Get latest attempt
    student_exam = StudentExam.objects.filter(
        student=request.user,
        exam=exam
    ).order_by('-id').first()

    # If no attempt exists, show message instead of redirect
    if not student_exam:
        return render(request, 'exam_result.html', {
            'exam': exam,
            'answers': [],
            'score': None,
            'total': 0,
            'message': 'You have not attempted this exam yet.'
        })

    # Get student's answers
    student_answers = StudentAnswer.objects.filter(student_exam=student_exam)
    answers = []

    for ans in student_answers:
        q = ans.question
        answers.append({
            'question': q,
            'selected': ans.selected_option,
            'correct': q.correct_option,
            'is_correct': ans.selected_option == q.correct_option
        })

    return render(request, 'exam_result.html', {
        'exam': exam,
        'answers': answers,
        'score': student_exam.score,
        'total': student_answers.count(),
        'message': ''
    })




def add_assignment(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        link = request.POST.get('material_link')
        due_date_str = request.POST.get('due_date')

        
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()

        
        if due_date < timezone.now().date():
            messages.error(request, "Due date cannot be in the past")
            return render(request, 'add_assignment.html', {'course': course})

        
        Assignment.objects.create(
            course=course,
            title=title,
            description=description,
            material_link=link,
            due_date=due_date
        )

        return redirect(f'/Courses/instructor/courses?tab=academics&course_id={course.id}&subtab=assignment')

    return render(request, 'add_assignment.html', {'course': course})

def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    submission = AssignmentSubmission.objects.filter(
        assignment=assignment,
        student=request.user
    ).first()

    if request.method == 'POST':
        link = request.POST.get('submission_link')

        AssignmentSubmission.objects.update_or_create(
            assignment=assignment,
            student=request.user,
            defaults={'submission_link': link}
        )

        return redirect('assignment_detail', assignment_id=assignment.id)

    return render(request, 'assignment_detail.html', {
        'assignment': assignment,
        'submission': submission
    })

def view_assignment_submissions(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    submissions = AssignmentSubmission.objects.filter(assignment=assignment)

    return render(request, 'assignment_submissions.html', {
        'assignment': assignment,
        'submissions': submissions
    })

def evaluate_submission(request, submission_id):
    submission = get_object_or_404(AssignmentSubmission, id=submission_id)

    if request.method == 'POST':
        score = request.POST.get('score')
        feedback = request.POST.get('feedback')

        submission.score = score
        submission.feedback = feedback
        submission.save()

        return redirect('view_assignment_submissions', assignment_id=submission.assignment.id)

    return render(request, 'evaluate_submission.html', {
        'submission': submission
    })

def add_material(request, course_id):
    course = get_object_or_404(Course, id=course_id)

  
    if not InstructorAllocation.objects.filter(
    course=course,
    instructor=request.user
    ).exists():
        return redirect('course_detail', id=course.id)

    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')

        StudyMaterial.objects.create(
            course=course,
            title=title,
            file=file
        )

        return redirect(f'/Courses/instructor/courses?tab=academics&course_id={course.id}&subtab=material')
    
    return render(request, 'add_material.html', {'course': course})

def view_materials(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    materials = StudyMaterial.objects.filter(course=course)

    return render(request, 'view_materials.html', {
        'course': course,
        'materials': materials
    })



def add_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        video = request.FILES.get('video')

        Lesson.objects.create(
            course=course,
            title=title,
            video=video
        )

        
        url = reverse('instructor_dashboard')
        return redirect(f"{url}?tab=academics&course_id={course.id}&subtab=lesson")

    return render(request, 'add_lesson.html', {
        'course': course
    })

def view_lessons(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course)

    return render(request, 'view_lessons.html', {
        'course': course,
        'lessons': lessons
    })


def mark_watched(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'watched': True}
    )

    return JsonResponse({'status': 'ok'})

def course_progress(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    total_lessons = Lesson.objects.filter(course=course).count()

    watched_lessons = Attendance.objects.filter(
        student=request.user,
        lesson__course=course,
        watched=True
    ).count()

    progress = 0
    if total_lessons > 0:
        progress = (watched_lessons / total_lessons) * 100

    return render(request, 'progress.html', {
        'course': course,
        'progress': progress,
        'watched': watched_lessons,
        'total': total_lessons
    })

def manage_content(request):
    lessons = Lesson.objects.all()
    exams = Exam.objects.all()
    assignments = Assignment.objects.all()
    materials = StudyMaterial.objects.all()

    return render(request, 'manage_content.html', {
        'lessons': lessons,
        'exams': exams,
        'assignments': assignments,
        'materials': materials
    })


def delete_lesson(request, id):
    lesson = Lesson.objects.get(id=id)
    lesson.delete()
    return redirect('manage_content')


def delete_exam(request, id):
    exam = Exam.objects.get(id=id)
    exam.delete()
    return redirect('manage_content')


def delete_assignment(request, id):
    assignment = Assignment.objects.get(id=id)
    assignment.delete()
    return redirect('manage_content')


def delete_material(request, id):
    material = StudyMaterial.objects.get(id=id)
    material.delete()
    return redirect('manage_content')

def instructor_assignments(request):
    assignments = Assignment.objects.all()

    return render(request, 'instructor_assignments.html', {
        'assignments': assignments
    })

def mark_attendance(request, lesson_id):
    if request.user.is_authenticated:
        lesson = get_object_or_404(Lesson, id=lesson_id)

        attendance, created = Attendance.objects.get_or_create(
            student=request.user,
            lesson=lesson
        )

        attendance.watched = True
        attendance.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})

def enrolled_courses(request):
    if not request.user.is_authenticated:
        return redirect('login')

    print("LOGGED USER:", request.user)

    enrollments = CoursePurchase.objects.filter(
        user=request.user,
        status__iexact='approved'
    ).select_related('course', 'batch')

    print("COUNT:", enrollments.count())

    return render(request, 'enrolled_courses.html', {
        'enrollments': enrollments
    })


def admin_view_exams(request):
    exams = Exam.objects.all()
    return render(request, 'admin_view_exams.html', {'exams': exams})


def admin_view_assignments(request):
    assignments = Assignment.objects.all()
    return render(request, 'admin_view_assignments.html', {'assignments': assignments})


def admin_view_materials(request):
    materials = StudyMaterial.objects.all()
    return render(request, 'admin_view_materials.html', {'materials': materials})

def contact_view(request):
    return render(request, 'contact.html')
