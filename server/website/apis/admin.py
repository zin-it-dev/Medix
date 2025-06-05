from django.contrib import admin
from django.contrib.auth.models import Permission

from .sec_models import User
from .models import Category, Course, Employee, EmployeeProxy
from .sec import UserAdmin
from .mixins import AdminMixin, MaxObjectsMixin
from .inlines import CourseInline


class CategoryAdmin(AdminMixin):
    inlines = [CourseInline]
    
    list_display = ["name", "is_active", "created_on", "created_by"]


class CourseAdmin(AdminMixin):
    list_display = ["title", "photo_image"]


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["user", "department"]


class EmployeeProxyAdmin(admin.ModelAdmin):
    readonly_fields = ["user", "department"]


admin.site.site_header = "MEDIX"
admin.site.site_title = "MEDIX Udemy"
admin.site.index_title = "Welcome to MEDIX Udemy"

admin.site.register(User, UserAdmin)
admin.site.register(Permission)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeProxy, EmployeeProxyAdmin)