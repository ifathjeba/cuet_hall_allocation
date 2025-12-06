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


STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]


class RoomApplication(models.Model):
    email = models.EmailField()
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)
    cgpa = models.FloatField()
    room_type = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES)
    room_number = models.CharField(max_length=10, blank=True, null=True)
    special_request = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    allocated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.email} - {self.room_type}"