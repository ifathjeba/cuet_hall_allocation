from django.db import models
from django.contrib.auth.models import User


class Hall(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name



GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

HALL_CHOICES = [
    ('shamshen_naher', 'Shamshen Naher Hall'),
    ('sufia_kamal', 'Sufia Kamal Hall'),
    ('tapose_rabeya', 'Tapose Rabeya Hall'),
]

ROOM_TYPE_CHOICES = [
    ('Standard Room (4 People)', 'Standard Room (4 People)'),
    ('Gono Room (6 People)', 'Gono Room (6 People)'),
]

YEAR_CHOICES = [
    ('1', '1st Year'),
    ('2', '2nd Year'),
    ('3', '3rd Year'),
    ('4', '4th Year'),
    ('5', '5th Year'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=[('student','Student'), ('authority','Authority')], default='student')
    
    # Personal Info
    student_id = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    
    # Academic Info
    department = models.CharField(max_length=50, blank=True, null=True)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES, blank=True, null=True)
    session = models.CharField(max_length=20, blank=True, null=True)


    def __str__(self):
        return self.user.username



class RoomApplication(models.Model):
    # Personal info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    # Academic info
    department = models.CharField(max_length=50)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)
    session = models.CharField(max_length=20)

    # Room preferences
    hall = models.CharField(max_length=50, choices=HALL_CHOICES)
    room_type = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES)
    room_number = models.CharField(max_length=10, blank=True, null=True)
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