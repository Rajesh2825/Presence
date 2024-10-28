from . import views
from django.urls import path

urlpatterns = [
     path('', views.home, name='home'),
     path('login_view/', views.login_view, name='login_view'),
     path('logout/', views.logout, name='logout'),
     
     path('faculty_dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
     path('register/', views.register, name='register'),
     path('train_face/', views.train_face, name='train_face'),
     path('view_attendance/', views.view_attendance, name='view_attendance'),
     path('student_attendance_detail/<int:student_id>/', views.student_attendance_detail, name='student_attendance_detail'),
     
     path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
     path('view_student_attendance/', views.view_student_attendance, name='view_student_attendance'),
     
     path('camera_view_in/', views.camera_view_in, name='camera_view_in'),
     path('mark_attendance_in/', views.mark_attendance_in, name="mark_attendance_in"),
     path('camera_view_out/', views.camera_view_out, name="camera_view_out"),
     path('mark_attendance_out/', views.mark_attendance_out, name="mark_attendance_out"),
     
     path('not_authorised/', views.not_authorised, name='not_authorised')
]
