from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, School, TutorRequest, Transaction, Rating


# specifies which info could be seen/edited in Django Admin Dahsboard
class UserAdmin (BaseUserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name',
                    'school', 'email', 'profile_pic', 'total_points', 'is_tutor', 'classes_taken', 'times_available', 'time_zone', 'rate', 'tutor_avg_rating', 'tutee_avg_rating', 'is_staff')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Other', {'fields': ('school', 'profile_pic', 'total_points', 'is_tutor', 'classes_taken', 'times_available', 'time_zone', 'rate', 'tutor_avg_rating', 'tutee_avg_rating',)}),)

class SchoolAdmin (admin.ModelAdmin):
    list_display = ('id', 'name')

class TutorRequestAdmin (admin.ModelAdmin):
    list_display = ('id', 'date_sent_request', 'tutor', 'tutee', 'tutor_date', 'tutor_start_time', 'tutor_end_time', 'class_name', 'location', 'tutor_comment', 'tutee_comment', 'accepted', 'tutor_confirm_completed', 'tutee_confirm_completed',
    'both_confirm_completed', 'tutor_confirm_paid', 'tutee_confirm_paid', 'both_confirm_paid')

class TransactionAdmin (admin.ModelAdmin):
    list_display = ('id', 'sent_from', 'sent_to', 'method', 'points', 'date_transaction_made')

class RatingAdmin (admin.ModelAdmin):
    list_display = ('id', 'date_rating_given', 'given_by', 'given_to', 'rating_type', 'rating', 'comment')

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(TutorRequest, TutorRequestAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Rating, RatingAdmin)
