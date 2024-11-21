"""
LLM used: ChatGPT 4o mini

Prompt:
I'm creating a relational data model to keep track of class attendance. Could you build the models.py file? These are the directions/specifications for the model:

An important part of data engineering development is to interpret and understand application specifications. Here we spec out what the attendance chip application needs to support.



User Management: There will be two classes of users: students and instructors. a. Students represent students who can take one or more course. Students have a student id number. b. Instructors represent course staff who can teach one or more course. Instructors have an instructor id number. c. The application should be able to add new students and instructors. 


Course Management: For simplicity, courses have only a single instructor, but instructors can teach multiple courses. a. Each course should have a course id number. b. The application should allow students to join a particular course. c. The application should allow an instructor to display a QR code for a particular course d. The application should create a custom upload dialog for pictures of the QR code. 


Post-hoc Analytics: All of the data in (1) and (2) should be stored in the database. a. Offline, we should be able to determine whether a student uploaded a valid QR code for a particular lecture b. Offline, we should be able to determine attendance for a particular lecture.

Don't worry about implementing the full functionality yet. Instead we want you to think about the data model, what data needs to be stored and how it needs to be linked. You will edit the file models.py to have your data model.

At a high level here are all the entities that you have:

-Users (of type either instructor or students) 
-Courses (instructors teach these and students take these) 
-Lectures (particular days for each course)
-QR Codes (uploads that are associated with lectures and students)
"""

from django.db import models

class User(models.Model):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    ]
    
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    class Meta:
        abstract = True  # This makes User an abstract model

class Student(User):
    student_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.username} (Student)"

class Instructor(User):
    instructor_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.username} (Instructor)"

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.course_name

class Lecture(models.Model):
    lecture_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    lecture_date = models.DateField()

    def __str__(self):
        return f"{self.course.course_name} on {self.lecture_date}"

class QRCode(models.Model):
    qr_code_id = models.AutoField(primary_key=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='qr_codes')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='qr_codes')
    qr_code_image = models.ImageField(upload_to='qr_codes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('lecture', 'student')

    def __str__(self):
        return f"QR Code for {self.student.username} in {self.lecture.course.course_name} on {self.lecture.lecture_date}"
