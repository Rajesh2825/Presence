from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Attendance

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_student', 'is_faculty', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_student', 'is_faculty')
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'is_student', 'is_faculty')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_student', 'is_faculty', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    ordering = ('username',)
    

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'roll_number')
    search_fields = ('user__username', 'name', 'roll_number')
    

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'check_in_time', 'check_out_time')
    list_filter = ('date', 'status')
    search_fields = ('student__user__username', 'student__roll_number')
    ordering = ('date',)