Django Web Voting App

A simple web voting application built with Django.

How to Use

Clone the repository

git clone https://github.com/marioskaraiskos/django-web-voting-app.git
cd django-web-voting-app


Create a virtual environment
For Windows:

python -m venv venv


For macOS/Linux:

python3 -m venv venv


Activate the virtual environment

Windows:

venv\Scripts\activate


macOS/Linux:

source venv/bin/activate


Install dependencies

pip install -r requirements.txt


Navigate to the project root

cd mysite


Run database migrations

python manage.py migrate


Start the development server

python manage.py runserver


Open your browser
Visit http://127.0.0.1:8000 to use the app.

Optional

Create a superuser to access the Django admin:

python manage.py createsuperuser
