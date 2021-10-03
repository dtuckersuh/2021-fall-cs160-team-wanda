from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User (AbstractUser):  # Custom User Model that inherits from Abstract User class
    # add additional fields
    first_name = models.CharField(max_length=100)  # first name field
    last_name = models.CharField(max_length=100)  # last name field
    email = models.EmailField(unique=True)  # email field, has to be unique
    school = models.CharField(max_length=100)
    profile_pic = models.ImageField(
        blank=True, upload_to="images/profile_pics", default="images/profile_pics/default_pic.png")  # store path to profile pic


class Tutor_Info(models.Model):  # Tutor Model storing tutor's information
    TIME_ZONES_CHOICES = (
        ('pacific', 'Pacific Time (PT)'),
        ('mountain', 'Mountain Time (MT)'),
        ('central', 'Central Time (CT)'),
        ('eastern', 'Eastern Time (ET)'),
    )

    # one-one relationship between user and tutor info
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    classes = models.TextField()
    times_available = models.TextField()
    timezone = models.CharField(
        max_length=8, choices=TIME_ZONES_CHOICES)
    rate = models.IntegerField()

    def __str__(self):
        return f'{self.user.username} Tutor Info'


class School(models.Model):  # Model storing all school names
    school_name = models.CharField(
        max_length=50, unique=True)  # fields must be unique

    def __str__(self):
        return self.school_name
