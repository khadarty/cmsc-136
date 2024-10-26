from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    instructor_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    course_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.name


class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    lecture_date = models.DateField()

    def __str__(self):
        return self.course


class QR_Code(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='qr_codes')
    qr_image = models.ImageField(upload_to='qr_codes/')

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