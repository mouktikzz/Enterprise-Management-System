# Enterprise Management System

## Overview
This is a Flask-based Enterprise Management System (EMS) that provides user authentication and management features for departments, employees, and projects. The application has been successfully imported and configured to run on Replit.

## Project Architecture

### Technology Stack
- **Backend Framework**: Flask 3.1.2
- **Database**: PostgreSQL (via Replit's built-in database)
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Authentication**: Flask-Login
- **Database Migrations**: Flask-Migrate (Alembic)
- **Production Server**: Gunicorn

### Project Structure
- `app/` - Main application package
  - `blueprints/` - Flask blueprints for different modules
    - `auth/` - User authentication (login/register)
    - `core/` - Core routes
    - `dashboard/` - Dashboard views
    - `departments/` - Department management
    - `employees/` - Employee management
    - `projects/` - Project management
  - `static/` - Static files (CSS)
  - `templates/` - Jinja2 HTML templates
  - `models.py` - Database models (User, Department, Employee, Project)
  - `extensions.py` - Flask extensions initialization
- `migrations/` - Database migration files
- `run.py` - Development server entry point
- `wsgi.py` - WSGI application entry point for production

### Database Models
- **User**: Authentication and authorization (includes role field)
- **Department**: Department management
- **Employee**: Employee records with department relationships
- **Project**: Project tracking with department relationships

## Recent Changes (November 16, 2025)
- Installed Python 3.11 and all required dependencies
- Configured PostgreSQL database connection using Replit's built-in database
- Ran database migrations to set up all tables
- Created `run.py` for development server bound to 0.0.0.0:5000
- Configured workflow to run the Flask application
- Set up deployment configuration using Gunicorn for production
- Added comprehensive `.gitignore` for Python projects
- Created this documentation file

## Configuration

### Environment Variables
- `SECRET_KEY` - Flask secret key (defaults to "dev" for development)
- `DATABASE_URL` - PostgreSQL connection string (automatically configured by Replit)

### Development Server
The application runs on `0.0.0.0:5000` in development mode with debug enabled.

### Production Deployment
Configured to use Gunicorn with autoscale deployment target, suitable for stateless web applications.

## Features
- User authentication (login/register)
- Role-based access control
- Department management (create, edit, list, view)
- Employee management (create, edit, list)
- Project management (create, edit, list)
- Dashboard for overview

## Current State
The application is fully functional and running. The database has been migrated and is ready for use. Users can register, login, and access all management features.
