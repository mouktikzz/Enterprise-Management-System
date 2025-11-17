# Enterprise Management System

## Overview
This is a comprehensive Flask-based Enterprise Management System (EMS) that provides user authentication, role-based access control, and complete task and project management features. The application follows modern web development practices with a clean, professional UI.

## Project Architecture

### Technology Stack
- **Backend Framework**: Flask 3.1.2
- **Database**: PostgreSQL (via Replit's built-in database)
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Authentication**: Flask-Login with role-based access control
- **Database Migrations**: Flask-Migrate (Alembic)
- **Production Server**: Gunicorn
- **UI/UX**: Modern CSS with card-based layouts, badges, and responsive design

### Project Structure
- `app/` - Main application package
  - `blueprints/` - Flask blueprints for different modules
    - `auth/` - User authentication (login/register)
    - `core/` - Core routes (homepage)
    - `dashboard/` - Enhanced dashboard with statistics
    - `departments/` - Department management (admin only)
    - `employees/` - Employee management (admin only)
    - `projects/` - Project management with progress tracking
    - `tasks/` - Complete task management system
  - `static/css/` - Modern styling with professional design
  - `templates/` - Jinja2 HTML templates
  - `models.py` - Database models
  - `decorators.py` - Role-based access control decorators
  - `extensions.py` - Flask extensions initialization
- `migrations/` - Database migration files
- `run.py` - Development server entry point
- `wsgi.py` - WSGI application entry point for production

### Database Models
- **User**: Authentication with role-based access (admin/employee)
- **Department**: Department organization
- **Employee**: Employee records with department relationships
- **Project**: Projects with task relationships and completion tracking
- **Task**: Complete task management with priorities, statuses, and due dates

## Key Features

### 1. Role-Based Access Control
- **Admin Role**: Full system access, can create/edit all entities
- **Employee Role**: View own tasks and projects, update task status
- First registered user automatically becomes admin

### 2. Enhanced Dashboard
- **Task Statistics Cards**:
  - Completed tasks today
  - Pending tasks
  - Overdue tasks
  - Tasks in progress
- **Admin-Only Metrics**:
  - Total employees
  - Departments count
  - Active projects
  - Total tasks
- **Recent Tasks Table**: Quick overview of latest activity
- **Quick Actions**: Context-aware action buttons

### 3. Complete Task Management
- Create, edit, and delete tasks (admin)
- Assign tasks to employees
- Set priority levels (Low, Medium, High)
- Track status (Pending, In Progress, Completed)
- Due date tracking with overdue indicators
- Employees can update their own task status
- Visual badges for priority and status
- Overdue task highlighting

### 4. Project Progress Tracking
- Visual progress bars showing task completion percentage
- Color-coded progress indicators:
  - Red (0-30%): Early stage
  - Orange (31-60%): In progress
  - Blue (61-99%): Near completion
  - Green (100%): Completed
- Timeline display with start/end dates
- Task count per project
- Status badges

### 5. Modern UI/UX
- Clean, professional gradient header
- Card-based layouts with shadows
- Color-coded badges for status and priority
- Responsive grid layouts
- Empty state messages
- Form validation with user feedback
- Hover effects and transitions

## User Guide for Beginners

### Getting Started
1. **Register an Account**:
   - Click "Register" in the navigation
   - First user becomes admin automatically
   - Subsequent users are employees by default

2. **Login**:
   - Use your username and password
   - You'll be redirected to the homepage

### Admin Workflow
1. **Create Departments**:
   - Navigate to Departments → Create Department
   - Add department name and description

2. **Create Projects**:
   - Navigate to Projects → Create Project
   - Set project name, status, dates, and department

3. **Create Tasks**:
   - Navigate to Tasks → Create New Task
   - Fill in task details:
     - Title (required)
     - Description
     - Assign to an employee
     - Set priority (Low/Medium/High)
     - Choose project
     - Set due date

4. **Monitor Progress**:
   - Check Dashboard for quick statistics
   - View Projects page for progress bars
   - Track overdue tasks

### Employee Workflow
1. **View Assigned Tasks**:
   - Navigate to Tasks
   - See only your assigned tasks

2. **Update Task Status**:
   - Click "Start" to begin work (Pending → In Progress)
   - Click "Complete" when done (In Progress → Completed)

3. **Check Dashboard**:
   - View your task statistics
   - See recent tasks
   - Track your overdue items

## Technical Details for Learning

### How Role-Based Access Works
```python
# Decorators in app/decorators.py
@admin_required  # Only admin users can access
@employee_or_admin_required  # Any logged-in user
```

### Database Relationships
- Projects have many Tasks
- Tasks belong to a Project (optional)
- Tasks assigned to Users
- Employees belong to Departments

### Progress Calculation
```python
# In Project model
def get_completion_percentage(self):
    if not self.tasks:
        return 0
    completed = sum(1 for task in self.tasks if task.status == 'completed')
    return int((completed / len(self.tasks)) * 100)
```

## Recent Changes (November 17, 2025)
### Initial Setup (Nov 16)
- Installed Python 3.11 and all dependencies
- Configured PostgreSQL database
- Set up development and production environments

### Task Management System (Nov 17)
- Added complete Task model with relationships
- Created tasks blueprint with CRUD operations
- Implemented role-based access control
- Added task status workflow (pending → in_progress → completed)
- Added status dropdown to task creation form

### Enhanced Dashboard (Nov 17)
- Added task statistics cards
- Implemented role-specific metrics
- Created recent tasks table
- Added quick action buttons

### Projects Enhancement (Nov 17)
- Added progress bars with color coding
- Implemented completion percentage calculation
- Enhanced project list UI

### Modern UI Design (Nov 17)
- Redesigned with professional card layouts
- Added color-coded badges and status indicators
- Implemented responsive grid layouts
- Created modern gradient header

### Admin User Management (Nov 17)
- Added "Create User" feature for admins
- Automatic secure password generation (10 characters)
- User credentials displayed only once for security
- Admins can create both admin and employee accounts
- Simplified employee onboarding workflow

## Configuration

### Environment Variables
- `SECRET_KEY` - Flask secret key (defaults to "dev")
- `DATABASE_URL` - PostgreSQL connection (auto-configured by Replit)

### Running the Application
- **Development**: Automatically runs via workflow on port 5000
- **Production**: Configured with Gunicorn for deployment

## Future Enhancements (Optional)
The following features from the original design document can be added:
- Interactive charts using Chart.js (pie, line, bar charts)
- Analytics page with productivity metrics
- Settings page for profile management
- Email notifications using Celery + Redis
- Weekly summary reports
- Advanced filtering and search

## Current State
✅ Full task management system operational  
✅ Role-based access control working  
✅ Dashboard with statistics cards  
✅ Projects with progress tracking  
✅ Modern, professional UI  
✅ Database fully migrated and configured  
✅ Ready for use and further development
