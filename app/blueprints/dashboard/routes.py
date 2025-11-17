from flask import render_template
from flask_login import login_required, current_user
from . import bp
from ...models import User, Department, Employee, Task, Project
from datetime import datetime, date


@bp.route('/')
@login_required
def index():
    if current_user.is_admin():
        all_tasks = Task.query.all()
        users = User.query.all()
        projects = Project.query.all()
    else:
        all_tasks = Task.query.filter_by(assigned_to=current_user.id).all()
        users = [current_user]
        projects = Project.query.join(Task).filter(Task.assigned_to == current_user.id).distinct().all()
    
    completed_tasks = [t for t in all_tasks if t.status == 'completed']
    pending_tasks = [t for t in all_tasks if t.status == 'pending']
    in_progress_tasks = [t for t in all_tasks if t.status == 'in_progress']
    overdue_tasks = [t for t in all_tasks if t.is_overdue()]
    
    today = date.today()
    completed_today = [t for t in completed_tasks if t.updated_at and t.updated_at.date() == today]
    
    counts = {
        'total_tasks': len(all_tasks),
        'completed': len(completed_tasks),
        'pending': len(pending_tasks),
        'in_progress': len(in_progress_tasks),
        'overdue': len(overdue_tasks),
        'completed_today': len(completed_today),
        'users': User.query.count(),
        'departments': Department.query.count(),
        'employees': Employee.query.count(),
        'projects': Project.query.count(),
    }
    
    recent_tasks = Task.query.order_by(Task.created_at.desc()).limit(5).all() if current_user.is_admin() else \
                   Task.query.filter_by(assigned_to=current_user.id).order_by(Task.created_at.desc()).limit(5).all()
    
    return render_template('dashboard/index.html', counts=counts, recent_tasks=recent_tasks)