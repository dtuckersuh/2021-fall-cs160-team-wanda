from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User (AbstractUser):  # Custom User Model that inherits from Abstract User class
    TIME_ZONES_CHOICES = (
        ('pacific', 'Pacific Time (PT)'),
        ('mountain', 'Mountain Time (MT)'),
        ('central', 'Central Time (CT)'),
        ('eastern', 'Eastern Time (ET)'),
    )

    # add additional fields
    first_name = models.CharField(max_length=100)  # first name field
    last_name = models.CharField(max_length=100)  # last name field
    email = models.EmailField(unique=True)  # email field, has to be unique
    school = models.CharField(max_length=100)
    profile_pic = models.ImageField(
        blank=True, upload_to="images/profile_pics", default="images/profile_pics/default_pic.png")  # store path to profile pic
    total_points = models.FloatField(default=0)
    is_tutor = models.BooleanField(default=False)
    classes_taken = models.TextField(null=True)
    times_available = models.TextField(null=True)
    time_zone = models.CharField(
        max_length=8, choices=TIME_ZONES_CHOICES, null=True)
    rate = models.IntegerField(null=True)
    average_rating = models.FloatField(null=True)

    def __str__(self):
        return f'{self.username} {self.is_tutor}'


class School(models.Model):  # Model storing all school names
    school_name = models.CharField(
        max_length=50, unique=True)  # fields must be unique

    def __str__(self):
        return self.school_name
