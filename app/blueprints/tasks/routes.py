from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from . import bp
from ...extensions import db
from ...models import Task, Project, User
from ...decorators import admin_required, employee_or_admin_required
from datetime import datetime


@bp.route('/')
@login_required
def list_tasks():
    if current_user.is_admin():
        tasks = Task.query.order_by(Task.due_date.asc()).all()
    else:
        tasks = Task.query.filter_by(assigned_to=current_user.id).order_by(Task.due_date.asc()).all()
    
    return render_template('tasks/list.html', tasks=tasks)


@bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        project_id = request.form.get('project_id')
        assigned_to = request.form.get('assigned_to')
        priority = request.form.get('priority', 'medium')
        due_date_str = request.form.get('due_date')
        
        if not title:
            flash('Task title is required')
            return redirect(url_for('tasks.create'))
        
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format')
                return redirect(url_for('tasks.create'))
        
        task = Task(
            title=title,
            description=description,
            project_id=int(project_id) if project_id else None,
            assigned_to=int(assigned_to) if assigned_to else None,
            priority=priority,
            due_date=due_date
        )
        
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully')
        return redirect(url_for('tasks.list_tasks'))
    
    projects = Project.query.all()
    users = User.query.filter_by(role='employee').all()
    return render_template('tasks/create.html', projects=projects, users=users)


@bp.route('/<int:task_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    
    if request.method == 'POST':
        task.title = request.form.get('title', '').strip()
        task.description = request.form.get('description', '').strip()
        
        project_id = request.form.get('project_id')
        task.project_id = int(project_id) if project_id else None
        
        assigned_to = request.form.get('assigned_to')
        task.assigned_to = int(assigned_to) if assigned_to else None
        
        task.priority = request.form.get('priority', 'medium')
        task.status = request.form.get('status', 'pending')
        
        due_date_str = request.form.get('due_date')
        if due_date_str:
            try:
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format')
                return redirect(url_for('tasks.edit', task_id=task_id))
        else:
            task.due_date = None
        
        db.session.commit()
        flash('Task updated successfully')
        return redirect(url_for('tasks.list_tasks'))
    
    projects = Project.query.all()
    users = User.query.all()
    return render_template('tasks/edit.html', task=task, projects=projects, users=users)


@bp.route('/<int:task_id>/update_status', methods=['POST'])
@employee_or_admin_required
def update_status(task_id):
    task = Task.query.get_or_404(task_id)
    
    if not current_user.is_admin() and task.assigned_to != current_user.id:
        flash('You can only update your own tasks')
        return redirect(url_for('tasks.list_tasks'))
    
    new_status = request.form.get('status')
    if new_status in ['pending', 'in_progress', 'completed']:
        task.status = new_status
        db.session.commit()
        flash(f'Task marked as {new_status.replace("_", " ")}')
    
    return redirect(url_for('tasks.list_tasks'))


@bp.route('/<int:task_id>/delete', methods=['POST'])
@admin_required
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully')
    return redirect(url_for('tasks.list_tasks'))
