from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True, null=True)
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    instructor_id = models.CharField(max_length=10, unique=True, null=True)
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True)
    # instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses', null=True)
    start_time = models.TimeField(null=True)  # Field to store start time of the course
    end_time = models.TimeField(null=True)    # Field to store end time of the course
    days_of_week = models.CharField(max_length=100, null=True)    # Field to store days of the week as a comma-separated string

    def __str__(self):
        return self.name


class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures', null=True)
    lecture_date = models.DateField(null=True)

    def __str__(self):
        return self.course


class QR_Code(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='qr_codes', null=True)
    qr_image = models.ImageField(upload_to='', null=True)
    #student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='qr_codes', null=True)
    student = models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lecture


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    qr_code = models.ForeignKey(QR_Code, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'qr_code')

    def __str__(self):
        return self.valid
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=False)
    #student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    #instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
