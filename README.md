# AFP Web App

## Basic Commands

Creating a project:

```bash
django-admin startproject afp_app
```

Run web app:

```bash
python manage.py runserver
```

Creating an app within the project:

```bash
cd afp_app
mkdir -p afp_app/accounts
python manage.py startapp accounts afp_app/accounts
```

Set up the database:

```bash
python manage.py migrate
```

Activate database models:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create admin user:

```bash
python manage.py createsuperuser
```

## User Permissions

- is_superuser: Michael
- is_staff: can log into admin pages (AFP Committee)
- is_physician: physician review
- is_scientist: clinician scientist review

## Navbar

- LH

  - CAMH Logo: all
  - Home: all
  - Awards: is_physician
  - Promotion: is_physician
  - Research: all
    - Grants: all
    - Grant Review: is_physician
    - Editorial Boards: is_physician
    - Publications: all
  - Education: is_physician
    - Committee Work
    - Lectures
    - Exams
    - Supervision

- RH
  - Admin: is_admin
  - Help: all
  - Profile: all
  - Logout: all
