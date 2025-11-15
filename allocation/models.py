from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=[('student','Student'), ('authority','Authority')], default='student')

    def __str__(self):
        return self.user.username


class Hall(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Application(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.hall.name}"


class RoomApplication(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    # Personal info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    university_id = models.CharField(max_length=50)  # renamed, do NOT use student_id
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)

    # Academic info
    faculty = models.CharField(max_length=200)
    year = models.CharField(max_length=10)
    session = models.CharField(max_length=20)

    # Room preferences
    hall = models.CharField(max_length=100)
    room_type = models.CharField(max_length=100)
    special_requests = models.TextField(blank=True, null=True)

    # Guardian info
    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=20)
    guardian_email = models.EmailField(blank=True, null=True)

    # System fields
    status = models.CharField(max_length=20, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.hall}"
