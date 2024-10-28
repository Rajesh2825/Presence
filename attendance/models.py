from django.contrib.auth.models import AbstractUser, Group, Permission
import json
from django.db import models

class User(AbstractUser):
    """Custom user model that extends Django's AbstractUser."""
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='attendance_user_set', 
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='attendance_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    roll_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='student_images/', blank=True, null=True)
    face_encoding = models.TextField(null=True, blank=True)  

    def set_face_encoding(self, encoding):
        self.face_encoding = json.dumps(encoding.tolist()) 
    def get_face_encoding(self):
        return json.loads(self.face_encoding)
    
    def __str__(self):
        return self.user.username

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"
    