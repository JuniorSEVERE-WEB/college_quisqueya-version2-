College Quisqueya
A modern school management system built with Django (backend) and Vite/React (frontend).

Features
User authentication (students, teachers, parents, employees, admin)
Student and teacher management
Enrollments and approvals
Report cards and grades
Donations management
Programs, sections, and classrooms
Modern Django admin interface (Jazzmin)
Easy customization for educational institutions
Tech Stack
Backend: Django, Django REST Framework, Jazzmin
Frontend: React, Vite
Getting Started
Backend
Clone the repository and navigate to the backend folder:

git clone https://github.com/JuniorSEVERE-WEB/college_quisqueya.git
cd college_quisqueya/backend
Create and activate a virtual environment:

python -m venv env
env\Scripts\activate  # On Windows
Install dependencies:

pip install -r requirements.txt
Run migrations and create a superuser:

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
Start the development server:

python manage.py runserver
Access the admin interface at http://localhost:8000/admin/

Frontend
Navigate to the frontend folder:

cd ../frontend
Install dependencies:

npm install
Start the development server:

npm run dev
License
This project is licensed under the MIT License.
