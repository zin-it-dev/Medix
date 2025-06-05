from django.contrib import admin

from .models import Course, Employee


class CourseInline(admin.StackedInline):
    model = Course
    
    
class EmployeeInline(admin.TabularInline):
    model = Employee
    can_delete = False
    verbose_name_plural = "employee"