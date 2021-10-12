from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, School


# specifies which info could be seen/edited in Django Admin Dahsboard
class UserAdmin (BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name',
                    'school', 'email', 'profile_pic', 'total_points', 'is_tutor', 'classes_taken', 'times_available', 'time_zone', 'rate', 'tutor_avg_rating', 'tutee_avg_rating', 'is_staff')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Other', {'fields': ('school', 'profile_pic', 'total_points', 'is_tutor', 'classes_taken', 'times_available', 'time_zone', 'rate', 'tutor_avg_rating', 'tutee_avg_rating',)}),)


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(School)
