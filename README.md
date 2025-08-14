# DjangoCraft - Project & Task Manager

A comprehensive Django-based project and task management system with team collaboration features.

## Features

- User registration, login, and role management (Admin, Project Manager, Team Member)
- Project creation, team management, and task assignment
- File uploads for tasks
- Advanced tagging and filtering
- Statistical dashboard (Chart.js/Plotly)
- REST API for mobile applications

## Tech Stack

- **Backend**: Django 5.2.5
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript
- **API**: Django REST Framework
- **Charts**: Chart.js/Plotly

## Setup Instructions

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `env_example.txt` to `.env` and configure your database settings
6. Run migrations: `python manage.py migrate`
7. Create superuser: `python manage.py createsuperuser`
8. Run the development server: `python manage.py runserver`

## Project Structure

```
DjangoCraft/
├── project_manager/     # Main project settings
├── core/               # Main application
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── .env               # Environment variables (create from env_example.txt)
```

## Development Progress

- [x] Project setup and configuration
- [x] PostgreSQL database configuration
- [x] Environment variables setup
- [ ] User authentication system
- [ ] Project and task models
- [ ] Team management
- [ ] File upload functionality
- [ ] Dashboard and statistics
- [ ] REST API
- [ ] Frontend templates