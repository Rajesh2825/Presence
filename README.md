# Face Recognition Attendance System for Students

A Django-based face recognition system to manage student attendance. Students can mark attendance using facial recognition, and both students and faculty have personalized dashboards to view attendance data. Faculty can see attendance records for all students on a daily basis.

## Features
- **Automated Attendance:** Students mark attendance with facial recognition, eliminating manual entries.
- **Check-In/Check-Out:** Both attendance "in" and "out" times are recorded.
- **Student Dashboard:** View personal attendance history.
- **Faculty Dashboard:** Faculty can view attendance data for all students.
- **Secure Storage:** Uses face encodings for privacy, backed by MySQL.

## Tech Stack
- **Backend:** Django 5.1.2
- **Database:** MySQL
- **Face Recognition:** OpenCV and Dlib
- **Frontend:** HTML, CSS, Bootstrap (via crispy forms)

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.11.6 (for compatibility with face recognition libraries)
- MySQL database
- pip (Python package installer)

### 1. Clone the Repository
```bash
git clone https://github.com/your-Rajesh2825/Presence.git
```
```bash
cd Presence
```
