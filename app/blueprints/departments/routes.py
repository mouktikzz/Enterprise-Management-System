from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from ...decorators import admin_required
from . import bp
from ...extensions import db
from ...models import Department


@bp.route('/')
def list_departments():
    items = Department.query.order_by(Department.name.asc()).all()
    return render_template('departments/list.html', items=items)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_department():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        if not name:
            flash('Name is required')
            return render_template('departments/create.html')
        if Department.query.filter_by(name=name).first():
            flash('Department already exists')
            return render_template('departments/create.html')
        dep = Department(name=name, description=description or None)
        db.session.add(dep)
        db.session.commit()
        return redirect(url_for('departments.list_departments'))
    return render_template('departments/create.html')


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_department(id):
    dep = Department.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        if not name:
            flash('Name is required')
            return render_template('departments/edit.html', item=dep)
        other = Department.query.filter(Department.name == name, Department.id != dep.id).first()
        if other:
            flash('Name already taken')
            return render_template('departments/edit.html', item=dep)
        dep.name = name
        dep.description = description or None
        db.session.commit()
        return redirect(url_for('departments.list_departments'))
    return render_template('departments/edit.html', item=dep)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_department(id):
    dep = Department.query.get_or_404(id)
    db.session.delete(dep)
    db.session.commit()
    return redirect(url_for('departments.list_departments'))

@bp.route('/<int:id>')
def detail(id):
    dep = Department.query.get_or_404(id)
    return render_template('departments/detail.html', item=dep)