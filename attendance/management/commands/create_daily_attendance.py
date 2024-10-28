from django.core.management.base import BaseCommand
from django.utils import timezone
from attendance.models import Attendance, Student  

class Command(BaseCommand):
    help = 'Create attendance records for all students for the current day'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()

        students = Student.objects.all()

        for student in students:
            attendance, created = Attendance.objects.get_or_create(
                student=student,
                date=today,
                defaults={
                    'check_in_time': None,  
                    'check_out_time': None,
                    'status': 'Absent'  
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created attendance record for {student.name} on {today}'))
            else:
                self.stdout.write(self.style.WARNING(f'Attendance record for {student.name} already exists for {today}'))
