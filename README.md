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
- **Deployment**: Docker, Nginx, Gunicorn

## Quick Start

### Option 1: Local Development
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `env_example.txt` to `.env` and configure your database settings
6. Run migrations: `python manage.py migrate`
7. Create superuser: `python manage.py createsuperuser`
8. Run the development server: `python manage.py runserver`

### Option 2: Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Access the application
# Web: http://localhost:8000
# Admin: http://localhost:8000/admin
```

## Project Structure

```
DjangoCraft/
├── project_manager/     # Main project settings
├── core/               # Main application
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
├── nginx.conf          # Nginx configuration
├── deployment_guide.md # Comprehensive deployment guide
├── export_project.sh   # Export script (Linux/Mac)
├── export_project.bat  # Export script (Windows)
└── .env               # Environment variables (create from env_example.txt)
```

## Export/Deployment

### Export Project
- **Linux/Mac**: Run `./export_project.sh`
- **Windows**: Run `export_project.bat`

This will create a clean export of your project with all necessary files for deployment.

### Production Deployment
See `deployment_guide.md` for detailed production deployment instructions including:
- Server setup
- Database configuration
- SSL/HTTPS setup
- Backup strategies
- Performance optimization

## Development Progress

- [x] Project setup and configuration
- [x] PostgreSQL database configuration
- [x] Environment variables setup
- [x] User authentication system
- [x] Project and task models
- [x] Team management
- [x] File upload functionality
- [x] Admin panel configuration
- [x] Signals and automation
- [x] Docker configuration
- [x] Deployment documentation
- [ ] Dashboard and statistics
- [ ] REST API
- [ ] Frontend templates

## Support

For detailed deployment instructions, troubleshooting, and best practices, see `deployment_guide.md`.