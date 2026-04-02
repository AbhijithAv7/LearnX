from django.db import models
from django.conf import settings
from Users.models import *

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=100)
    price = models.IntegerField(null=True, blank=True) 
    image = models.ImageField(upload_to='courses/',blank=True, null=True)       
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class CourseAllocation(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.instructor} - {self.course} ({self.batch})"

class CoursePurchase(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.status}"
    

class StaffAllocation(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.CharField(max_length=50)
    allocated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff.name} → {self.course.title} ({self.batch})"
    
class InstructorAllocation(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.instructor.username} - {self.course.title}"


class Batch(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.name}"

