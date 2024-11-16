from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

#Users (of type either instructor or students)
#Courses (instructors teach these and students take these)
#Lectures (particular days for each course)
#QR Codes (uploads that are associated with lectures and students)

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        INSTRUCTOR = 'INSTRUCTOR', 'Instructor'
        STUDENT = 'STUDENT', 'Student'
    base_role = Role.STUDENT
    role = models.CharField('Role', max_length = 50, choices = Role.choices)

    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions_set", blank=True)


    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)
        
        

class Course(models.Model):
    name = models.CharField(max_length=256, primary_key=True)
    number = models.CharField(max_length=5)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to = {'role' : User.Role.INSTRUCTOR}, related_name="instructor_course")
    students = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to = {'role' : User.Role.STUDENT}, related_name="student_course") 
    def __str__(self):
        return self.name


class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name="lecture_for_course")
    lecture_name = models.CharField(max_length=256)
    lecture_date = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.course.name}: {self.lecture_name}'


class QRCode(models.Model):
    lectures = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name="lecture_qrcode")
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to = {'role' : User.Role.STUDENT}, related_name="student_qrcode")
    upload_time = models.DateTimeField(auto_now_add = True)
    img = models.ImageField(upload_to='images/')
    def __str__(self):
        return f'{self.student}: {self.upload_time}'