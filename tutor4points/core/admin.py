from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, School, Tutor_Info


# specifies which info could be seen/edited in Django Admin Dahsboard
class UserAdmin (BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name',
                    'school', 'email', 'profile_pic', 'tutor_info', 'is_staff')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Other', {'fields': ('school',)}),)


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(School)
admin.site.register(Tutor_Info)
