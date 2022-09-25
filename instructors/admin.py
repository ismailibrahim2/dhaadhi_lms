from django.contrib import admin
from .models import Instructor


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['user', 'qualification', 'mobile_phone', 'status']
    list_filter = ['status']
