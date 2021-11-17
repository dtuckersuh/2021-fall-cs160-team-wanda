from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class School(models.Model):  # Model storing all school names
    name = models.CharField(
        max_length=50, unique=True)  # fields must be unique

    def __str__(self):
        return f"{self.name}"


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
    classes_taken = models.TextField(null=True, blank=True)
    times_available = models.TextField(null=True, blank=True)
    time_zone = models.CharField(
        max_length=8, choices=TIME_ZONES_CHOICES, null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)
    tutor_avg_rating = models.FloatField(null=True, blank=True)
    tutee_avg_rating = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name.title()} {self.last_name.title()}'


class TutorRequest (models.Model):
    # automatically set date every time object is created
    date_sent_request = models.DateTimeField(auto_now_add=True)
    tutor = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL, related_name='tutor')
    tutee = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL)
    tutor_date = models.DateField()
    tutor_start_time = models.TimeField()
    tutor_end_time = models.TimeField()
    class_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    tutor_comment = models.TextField(null=True, blank=True)
    tutee_comment = models.TextField(null=True, blank=True)
    accepted = models.BooleanField(null=True)  # null by default
    completed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)


class Transaction (models.Model):
    METHODS = (
        ('purchase', 'PURCHASE'),
        ('transfer', 'TRANSFER'),
        ('cash_out', 'CASH_OUT'),
    )

    # automatically set date every time object is created
    date_transaction_made = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=25, choices=METHODS)
    points = models.FloatField()
    sent_from = models.ForeignKey(
        get_user_model(), null=True, blank = True, on_delete=models.SET_NULL, related_name='sent_from')
    sent_to = models.ForeignKey(
        get_user_model(), null=True, blank = True, on_delete=models.SET_NULL, related_name='sent_to')


class Rating (models.Model):
    RATING_TYPES = (
        ('tutee', 'TUTEE'),
        ('tutor', 'TUTOR')
    )

    # automatically set date every time object is saved
    date_rating_given = models.DateTimeField(auto_now=True)
    given_by = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL, related_name='given_by')
    given_to = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL)
    rating_type = models.CharField(max_length=5, choices=RATING_TYPES)
    rating = models.IntegerField(null=True, validators=[
                                 MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    