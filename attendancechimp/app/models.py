from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
import random
import string

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
    name = models.CharField(max_length=100, null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    days_of_week = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures', null=True)
    lecture_date = models.DateField(null=True)
    qrdata = models.CharField(max_length=16, blank=True, null=True)  # Added qrdata field

    def __str__(self):
        return self.course


class QR_Code(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='qr_codes', null=True)
    qr_image = models.ImageField(upload_to='', null=True)
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
        return str(self.valid)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


def getUploadsForCourse(course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        raise ObjectDoesNotExist("Course with the given ID does not exist")

    attendance_records = Attendance.objects.filter(
        lecture__course=course,
        valid=True
    ).select_related('student').annotate(
        username=F('student__name')
    ).values('username', 'upload_time')

    return [{'username': record['username'], 'upload_time_as_string': str(record['upload_time'])} for record in attendance_records]


