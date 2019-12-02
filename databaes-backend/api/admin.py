from django.contrib import admin
from .models import User, Student
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class StudentProfileInline (admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'student'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (StudentProfileInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
