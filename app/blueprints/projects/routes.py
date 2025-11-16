from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from . import bp
from ...extensions import db
from ...models import Project, Department
from datetime import datetime


@bp.route('/')
def list_projects():
    items = Project.query.order_by(Project.name.asc()).all()
    return render_template('projects/list.html', items=items)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_project():
    departments = Department.query.order_by(Department.name.asc()).all()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        status = request.form.get('status', '').strip()
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        department_id = request.form.get('department_id')
        if not name:
            flash('Name is required')
            return render_template('projects/create.html', departments=departments)
        dep = Department.query.get(department_id) if department_id else None
        def parse_date(s):
            try:
                return datetime.strptime(s, '%Y-%m-%d').date() if s else None
            except Exception:
                return None
        proj = Project(
            name=name,
            status=status or None,
            start_date=parse_date(start_date),
            end_date=parse_date(end_date),
            department=dep,
        )
        db.session.add(proj)
        db.session.commit()
        return redirect(url_for('projects.list_projects'))
    return render_template('projects/create.html', departments=departments)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    proj = Project.query.get_or_404(id)
    departments = Department.query.order_by(Department.name.asc()).all()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        status = request.form.get('status', '').strip()
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        department_id = request.form.get('department_id')
        if not name:
            flash('Name is required')
            return render_template('projects/edit.html', item=proj, departments=departments)
        def parse_date(s):
            try:
                return datetime.strptime(s, '%Y-%m-%d').date() if s else None
            except Exception:
                return None
        dep = Department.query.get(department_id) if department_id else None
        proj.name = name
        proj.status = status or None
        proj.start_date = parse_date(start_date)
        proj.end_date = parse_date(end_date)
        proj.department = dep
        db.session.commit()
        return redirect(url_for('projects.list_projects'))
    return render_template('projects/edit.html', item=proj, departments=departments)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_project(id):
    proj = Project.query.get_or_404(id)
    db.session.delete(proj)
    db.session.commit()
    return redirect(url_for('projects.list_projects'))