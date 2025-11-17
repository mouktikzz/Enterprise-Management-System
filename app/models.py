from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(32), default='employee', nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = db.relationship('Department', backref=db.backref('employees', lazy=True))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    status = db.Column(db.String(32))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = db.relationship('Department', backref=db.backref('projects', lazy=True))

    def get_completion_percentage(self):
        if not self.tasks:
            return 0
        completed = sum(1 for task in self.tasks if task.status == 'completed')
        return int((completed / len(self.tasks)) * 100)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    priority = db.Column(db.String(20), default='medium')
    status = db.Column(db.String(32), default='pending')
    due_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = db.relationship('Project', backref=db.backref('tasks', lazy=True))
    assignee = db.relationship('User', backref=db.backref('tasks', lazy=True))

    def is_overdue(self):
        if self.due_date and self.status != 'completed':
            return datetime.now().date() > self.due_date
        return False

    def get_priority_badge_class(self):
        priority_classes = {
            'low': 'success',
            'medium': 'warning',
            'high': 'danger'
        }
        return priority_classes.get(self.priority, 'secondary')

    def get_status_badge_class(self):
        status_classes = {
            'pending': 'secondary',
            'in_progress': 'info',
            'completed': 'success'
        }
        return status_classes.get(self.status, 'secondary')