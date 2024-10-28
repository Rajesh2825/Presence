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
git clone https://github.com/Rajesh2825/Presence.git
```
```bash
cd Presence
```


###2. Create a virtual environment (recommended):
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `.\env\Scripts\activate`
    ```

###3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

###4. Set up environment variables: Create a `project.env` file in the project root with the following structure:
    ```plaintext
    SECRET_KEY=your_django_secret_key
    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_HOST=localhost
    DB_PORT=3306
    ```

###5. Set up your MySQL database:
   - Open MySQL and create a database named `face_recognition_attendance`:
     ```sql
     CREATE DATABASE face_recognition_attendance;
     ```
###6. Create a Faculty Account:
   - Create a faculty user with is_faculty = True in your Django admin panel or via the Django shell. Here’s how to do it via the shell:
     ```bash
     python manage.py shell
     ```
     Then run:
     ```bash
     from attendance.models import User
     ```
     ```bash
     User.objects.create_user(username='faculty_username', password='faculty_password', is_faculty=True)
     ```
     Replace 'faculty_username' and 'faculty_password' with desired credentials.


###7. Apply migrations:
    ```bash
    python manage.py makemigrations
    ```
    ```bash
     python manage.py migrate
    ```

###8. Run the development server:
    ```bash
    python manage.py runserver
    ```

###9. Visit `http://127.0.0.1:8000` to see the website in action.

###10. Register Student with there face image:
  1. Log in to the Faculty dashboard with your faculty credentials.
  2. Navigate to the Register Student section and add new students with there image.

###11. Train Face Recognition Model for Added Students:
  - After adding students, you will need to train the system with their face:
    - for that you need to click on start training in faculty dashboard.
    - it will take you to train_face page you need to wait until its train face.

###12. Now, you are ready to scan students faces and make attendance in and out.

## Usage
- **Marking Attendance:** Student can mark there attendance in and out using its face scanning.
- **Student Login:** Students log in with their credentials to access their dashboard and view attendance records.
- **Faculty Login:** Faculty log in with admin permissions to view and manage all student attendance records.


## Screenshots

### Home Page
![Home Page](website_img/homepage.png)

### Product Page
![Product Page](website_img/product.png)

### Shoping Page
![Product Page](website_img/shop.png)

### Wish list Page
![Shopping Cart](website_img/wishlist.png)

### Shoping Cart Page
![Admin Panel](website_img/cart.png)

### Checkout Page
![Admin Panel](website_img/checkout.png)

### Payment Page
![Admin Panel](website_img/payment.png)

### Confirm Order Page
![Admin Panel](website_img/confirm_order.png)

### Orders Page
![Admin Panel](website_img/order.png)



## Contributing
Contributions are welcome! Please fork the repository and create a pull request for any changes or improvements.

## License
This project is licensed under the [MIT License](https://github.com/sibtc/django-multiple-user-types-example/blob/master/LICENSE).

## Contact
For any queries, please contact:

**Author:** Radadiya Rajesh
