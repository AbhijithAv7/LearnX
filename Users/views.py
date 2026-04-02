from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from Dashboard.views import *
from django.contrib.auth import logout
User = get_user_model()

def role_select(request):
    return render(request, 'role_select.html')


def register(request, role):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phonenumber']
        password = request.POST['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        
        user.role = role   
        user.save()

        
        return redirect('login')

    return render(request, 'register.html', {'role': role})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'instructor':
                return redirect('instructor_dashboard')
            elif user.role == 'staff':
                return redirect('staff_dashboard')
            else:
                return redirect('home')

        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'login.html')

def view_students(request):
    students = User.objects.filter(role='student')
    return render(request, 'view_students.html', {'students': students})


def view_staff(request):
    staff = User.objects.filter(role='staff')
    return render(request, 'view_staff.html', {'staff': staff})


def view_instructors(request):
    instructors = User.objects.filter(role='instructor')
    return render(request, 'view_instructors.html', {'instructors': instructors})

def update_user(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        return redirect('admin_dashboard')  

    return render(request, 'update_user.html', {'user': user})


def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('admin_dashboard')

def user_logout(request):
    logout(request)
    return redirect('home')
