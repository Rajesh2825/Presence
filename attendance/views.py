import base64
from io import BytesIO
import json
import time
from PIL import Image
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import cv2
from datetime import datetime
from calendar import month_name
import face_recognition
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import numpy as np
from django.utils import timezone
from .forms import LoginForm, StudentRegisterForm
from .models import Student, Attendance

# homepage and login related views....

def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_student:
                    return redirect('/student_dashboard/')  
                elif user.is_faculty:
                    return redirect('/faculty_dashboard/')  
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required(login_url='/login_view/')
def logout(request):
    auth_logout(request)
    return redirect("/")




# faculty and its related views...

@login_required(login_url='/login_view/')
def faculty_dashboard(request):
    if request.user.is_faculty:
        total_students = Student.objects.count()

        today = timezone.now().date()

        total_present = Attendance.objects.filter(date=today, status='present').count()
        total_absent = total_students - total_present 
        attendance_percentage = (total_present / total_students * 100) if total_students > 0 else 0

        context = {
            'total_students': total_students,
            'total_present': total_present,
            'total_absent': total_absent,
            'attendance_percentage': attendance_percentage,
        }
        return render(request, 'faculty_dashboard.html', context)

    return redirect('/not_authorised/')


@login_required(login_url='/login_view/')
def register(request):
    if request.user.is_faculty: 
        if request.method == 'POST':
            form = StudentRegisterForm(request.POST, request.FILES)
            if form.is_valid():
                form.save() 
                return redirect('/faculty_dashboard/')
            else:
                messages.error(request, "Invalid form submission.")
        else:
            form = StudentRegisterForm()
        
        return render(request, 'register.html', {'form': form})
    
    return redirect('/not_authorised/')


@login_required(login_url='/login_view/')
def train_face(request):
    if request.user.is_faculty: 
        if request.method == 'GET':
            return render(request, 'train_face.html')
        elif request.method == 'POST':
            try:
                students = Student.objects.all()

                for student in students:
                    if student.image:  
                        uploaded_image = face_recognition.load_image_file(student.image.path)
                        encoding = face_recognition.face_encodings(uploaded_image)
                        if encoding:
                            student.set_face_encoding(encoding[0]) 
                            student.save()
                return JsonResponse({'redirect_url': '/faculty_dashboard/'}) 
            except Exception as e:
                messages.error(request, f"An error occurred during training: {str(e)}")
                return redirect('/train_face/')
            
    return redirect('/not_authorised/')


@login_required(login_url='/login_view/')
def view_attendance(request):
    if request.user.is_faculty:
        current_month = request.GET.get('month')
        if not current_month:
            current_month = datetime.now().month
        else:
            current_month = int(current_month)
        
        current_month_name = month_name[current_month]

        student_name = request.GET.get('student_name', '')

        students_attendance = []
        
        students = Student.objects.all()
        if student_name:
            students = students.filter(name__icontains=student_name)

        for student in students:
            attendance_records = Attendance.objects.filter(
                student=student,
                date__month=current_month
            )
            
            if attendance_records.exists():
                present_days = attendance_records.filter(status='present').count()
                total_days = attendance_records.count()
                absent_days = total_days - present_days
                
                if total_days > 0:
                    present_percentage = (present_days / total_days) * 100
                else:
                    present_percentage = 0

                students_attendance.append({
                    'name': student.name,
                    'id': student.id,
                    'present_days': present_days,
                    'absent_days': absent_days,
                    'present_percentage': round(present_percentage, 2)
                })
        months = [(i, month_name[i]) for i in range(1, 13)]


        return render(request, 'view_attendance.html', {
            'students_attendance': students_attendance,
            'current_month': current_month_name,
            'selected_student_name': student_name,
            'selected_month': current_month,
            'months': months,
        })

    return redirect('/not_authorised/')


@login_required(login_url='/login_view/')
def student_attendance_detail(request, student_id):
    if request.user.is_faculty:
        student = Student.objects.get(id=student_id)
        date = request.GET.get('date', '')
        month = request.GET.get('month', '')
        year = request.GET.get('year', '')

        attendance_records = Attendance.objects.filter(student=student)

        if date:
            attendance_records = attendance_records.filter(date=date)
        if month:
            attendance_records = attendance_records.filter(date__month=month)
        if year:
            attendance_records = attendance_records.filter(date__year=year)
        context = {
            'attendance_records': attendance_records,
            'name': student,
            'student_id': student_id,
        }

        return render(request, 'student_attendance_detail.html', context)
    
    return redirect('/not_authorised/')
   
     



# Student and its related views.....

@login_required(login_url='/login_view/')
def student_dashboard(request):
    if request.user.is_student:
        student = request.user.student 
        
        attendance_records = Attendance.objects.filter(student=student)

        total_days = attendance_records.count()
        present_days = attendance_records.filter(status='Present').count()  
        absent_days = total_days - present_days
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0


        context = {
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': absent_days,
            'attendance_percentage': attendance_percentage,
        }

        return render(request, 'student_dashboard.html', context)
    return redirect('/not_authorised/')

@login_required(login_url='/login_view/')
def view_student_attendance(request):
    if request.user.is_student:
        student = request.user.student
        
        date = request.GET.get('date', '')
        month = request.GET.get('month', '')
        year = request.GET.get('year', '')

        attendance_records = Attendance.objects.filter(student=student)

        if date:
            attendance_records = attendance_records.filter(date=date)
        if month:
            attendance_records = attendance_records.filter(date__month=month)
        if year:
            attendance_records = attendance_records.filter(date__year=year)

        context = {
            'attendance_records': attendance_records,
        }

        return render(request, 'view_student_attendance.html', context)
    return redirect('/not_authorised/')




# attendance in and out views.....

def mark_attendance_in(request):
    if request.method == 'GET':
        try:
            face_classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
            
            video_capture = cv2.VideoCapture(0)
            
            def detect_bounding_box(vid):
                gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
                return faces
            
            students = Student.objects.exclude(face_encoding__isnull=True)
            student_encodings = []

            for student in students:
                encoding = student.get_face_encoding()  
                student_encodings.append((encoding, student))
                marked_students = set()
            
            while True:

                    result, video_frame = video_capture.read() 
                    if result is False:
                        break 

                    faces = detect_bounding_box(
                        video_frame
                    )
                    
                    
                    if len(faces) > 0:
                        rgb_frame = cv2.cvtColor(video_frame, cv2.COLOR_BGR2RGB)
                        face_locations = face_recognition.face_locations(rgb_frame)
                        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                        for (face_encoding, face_location) in zip(face_encodings, face_locations):
                            matches = face_recognition.compare_faces([encoding[0] for encoding in student_encodings], face_encoding)

                            if True in matches:
                                first_match_index = matches.index(True)
                                matched_student = student_encodings[first_match_index][1]

                                if matched_student.id not in marked_students:
                                    mark_attendance_in_db(matched_student.user)
                                    marked_students.add(matched_student.id)

                                (top, right, bottom, left) = face_location 
                                cv2.rectangle(video_frame, (left, top), (right, bottom), (0, 255, 0), 2)
                                cv2.putText(video_frame, matched_student.name, 
                                            (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                            else:
                                (top, right, bottom, left) = face_location
                                cv2.rectangle(video_frame, (left, top), (right, bottom), (0, 0, 255), 2)
                                cv2.putText(video_frame, "No Match Found", 
                                            (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                                            
                    cv2.imshow(
                        "Attendance System", video_frame
                    ) 
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
            video_capture.release()
            cv2.destroyAllWindows()
            return redirect('/') 
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return redirect('/') 
    else:
        print("Invalid request method.")
        return redirect('/') 
        
def mark_attendance_in_db(user):
    try:
        student = Student.objects.get(user=user)

        today = timezone.now().date()

        attendance_record, created = Attendance.objects.get_or_create(
            student=student,
            date=today,
            defaults={'check_in_time': timezone.now(), 'status': 'present'}
        )

        if not created:
            if attendance_record.status == 'present':
                return JsonResponse({
                    'status': 'success',
                    'message': f"Attendance already marked for {student.name} on {today}."
                })
            else:
                attendance_record.status = 'present'
                attendance_record.check_in_time = timezone.now()
                attendance_record.save()
                return JsonResponse({
                    'status': 'success',
                    'message': f"Attendance marked for {student.name} on {today}."
                })
        else:
            return JsonResponse({
                'status': 'success',
                'message': f"Attendance marked for {student.name} on {today}."
            })

    except Student.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': "Student does not exist."
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f"An error occurred while marking attendance: {str(e)}"
        }, status=500)
        
        
        
def mark_attendance_out(request):
    if request.method == 'GET':
        try:
            face_classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
            
            video_capture = cv2.VideoCapture(0)
            
            def detect_bounding_box(vid):
                gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
                return faces
            
            students = Student.objects.exclude(face_encoding__isnull=True)
            student_encodings = []

            for student in students:
                encoding = student.get_face_encoding()  
                student_encodings.append((encoding, student))
                marked_students = set()
            
            while True:

                    result, video_frame = video_capture.read() 
                    if result is False:
                        break 

                    faces = detect_bounding_box(
                        video_frame
                    )
                    
                    
                    if len(faces) > 0:
                        rgb_frame = cv2.cvtColor(video_frame, cv2.COLOR_BGR2RGB)
                        face_locations = face_recognition.face_locations(rgb_frame)
                        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                        for (face_encoding, face_location) in zip(face_encodings, face_locations):
                            matches = face_recognition.compare_faces([encoding[0] for encoding in student_encodings], face_encoding)

                            if True in matches:
                                first_match_index = matches.index(True)
                                matched_student = student_encodings[first_match_index][1]

                                if matched_student.id not in marked_students:
                                    mark_attendance_out_db(matched_student.user)
                                    marked_students.add(matched_student.id)

                                (top, right, bottom, left) = face_location 
                                cv2.rectangle(video_frame, (left, top), (right, bottom), (0, 255, 0), 2)
                                cv2.putText(video_frame, matched_student.name, 
                                            (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                            else:
                                (top, right, bottom, left) = face_location
                                cv2.rectangle(video_frame, (left, top), (right, bottom), (0, 0, 255), 2)
                                cv2.putText(video_frame, "No Match Found", 
                                            (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                                            
                    cv2.imshow(
                        "Attendance System", video_frame
                    ) 
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
            video_capture.release()
            cv2.destroyAllWindows()
            return redirect('/') 
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return redirect('/') 
    else:
        print("Invalid request method.")
        return redirect('/') 
    
def mark_attendance_out_db(user):
    try:
        student = Student.objects.get(user=user)
        today = timezone.now().date()

        attendance_record = Attendance.objects.filter(student=student, date=today).first()

        if attendance_record.check_in_time:
            if attendance_record.check_out_time:
                return JsonResponse({
                "status": "success",
                "message": f"Check-out already marked for {student.name} on {today}."
                })
            else:
                attendance_record.check_out_time = timezone.now()
                attendance_record.save()
                return JsonResponse({
                "status": "success",
                "message": f"Check-out marked for {student.name} on {today}."
                })
        else:
            return JsonResponse({
            "status": "error",
            "message": f"No check-in record found for {student.name} on {today}. Cannot mark check-out."
            })
            
    except Student.DoesNotExist:
        return JsonResponse({
        "status": "error",
        "message": "Student does not exist."
        }, status=404)
    except Exception as e:
        return JsonResponse({
        "status": "error",
        "message": f"An error occurred while marking attendance: {str(e)}"
        }, status=500)
        
        
        
        
# not authorised view.....        

def not_authorised(request):
    return render(request, 'not_authorised.html')
