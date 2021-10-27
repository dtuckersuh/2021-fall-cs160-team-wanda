from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class School(models.Model):  # Model storing all school names
    name = models.CharField(
        max_length=50, unique=True)  # fields mu{% csrf_token %}st be unique

    def __str__(self):
        return self.name


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
    school = models.ForeignKey(School, null=True, on_delete=models.SET_NULL)
    profile_pic = models.ImageField(
        blank=True, upload_to="images/profile_pics", default="images/profile_pics/default_pic.png")  # store path to profile pic
    total_points = models.FloatField(default=0)
    is_tutor = models.BooleanField(default=False)
    classes_taken = models.TextField(null=True)
    times_available = models.TextField(null=True)
    time_zone = models.CharField(
        max_length=8, choices=TIME_ZONES_CHOICES, null=True)
    rate = models.IntegerField(null=True)
    tutor_avg_rating = models.FloatField(null=True)
    tutee_avg_rating = models.FloatField(null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class tutor_request (models.Model):
    class_name = models.CharField(max_length=100)
    # automatically set date every time object is saved
    date_requested = models.DateField(auto_now=True)
    tutor_date = models.DateField()
    location = models.CharField(max_length=100)
    time = models.TimeField()
    tutor = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL, related_name='tutor')
    tutee = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL)
    accepted = models.BooleanField(null=True)  # null by default
    completed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)


class transaction (models.Model):
    PAYMENT_METHODS = (
        ('visa', 'VISA'),
        ('points', 'POINTS'),
    )
    points = models.FloatField()
    method = models.CharField(max_length=25, choices=PAYMENT_METHODS)
    sent_to = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL)
    sent_from = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL, related_name='sent_from')
    date = models.DateField()


class rating (models.Model):
    RATING_TYPES = (
        ('tutee', 'TUTEE'),
        ('tutor', 'TUTOR')
    )

    type = models.CharField(max_length=5, choices=RATING_TYPES)
    rating = models.IntegerField(null=True, validators=[
                                 MinValueValidator(0), MaxValueValidator(5)])
    # automatically set date every time object is saved
    date = models.DateField(auto_now=True)
    given_by = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL, related_name='given_by')
    given_to = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL)
    comment = models.TextField()
