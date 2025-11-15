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


class RoomApplication(models.Model):
    # Personal info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)

    # Academic info
    department = models.CharField(max_length=50)
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
        return f"{self.student_id} - {self.hall}"
