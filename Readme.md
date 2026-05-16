# Employee Management — Minimal Django App

A small, easy-to-run Django project for managing employees and departments. This README explains how to get the project running locally, where the main pieces live, and how to run tests.

This file is written plainly so you (or another developer) can pick up the repo quickly.

---

## What this is

- A lightweight Django app (app name: `employee`) inside the `employee_management` project.
- Provides basic authentication (signup/login/logout), a dashboard, and simple CRUD for employees and departments.
- Designed to be minimal, readable, and easy to run locally.

## Prerequisites

- Python 3.11+ (project was developed on 3.11)
- Virtual environment recommended
- No external services required — uses SQLite (`db.sqlite3`) by default.

## Setup

1. Create and activate a virtual environment (if you haven't):

```cmd
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```cmd
pip install -r requirements.txt
```

3. Apply migrations and create a superuser (optional):

```powershell
venv\Scripts\python.exe employee_management\manage.py migrate
venv\Scripts\python.exe employee_management\manage.py createsuperuser
```

4. Run the development server:

```powershell
venv\Scripts\python.exe employee_management\manage.py runserver
```

5. Open your browser to `http://127.0.0.1:8000/` — the dashboard requires login.



## Project layout (important files)

- `employee_management/` — Django project config
  - `settings.py` — main settings (look for `LOGIN_REDIRECT_URL`)
  - `urls.py` — root URL config
- `employee/` — app
  - `models.py` — `Employee`, `Department` models
  - `forms.py` — signup and employee/department forms
  - `views.py` — dashboard, auth helpers, CRUD views
  - `urls.py` — app routes
  - `templates/` — HTML templates (includes `base.html` and `employees/` templates)

# Employee Management with System autentication