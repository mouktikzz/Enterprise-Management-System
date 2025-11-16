from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from . import bp
from ...extensions import db
from ...models import Employee, Department


@bp.route('/')
def list_employees():
    items = Employee.query.order_by(Employee.name.asc()).all()
    return render_template('employees/list.html', items=items)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_employee():
    departments = Department.query.order_by(Department.name.asc()).all()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        department_id = request.form.get('department_id')
        if not name:
            flash('Name is required')
            return render_template('employees/create.html', departments=departments)
        if email and Employee.query.filter_by(email=email).first():
            flash('Email already exists')
            return render_template('employees/create.html', departments=departments)
        dep = Department.query.get(department_id) if department_id else None
        emp = Employee(name=name, email=email or None, department=dep)
        db.session.add(emp)
        db.session.commit()
        return redirect(url_for('employees.list_employees'))
    return render_template('employees/create.html', departments=departments)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    emp = Employee.query.get_or_404(id)
    departments = Department.query.order_by(Department.name.asc()).all()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        department_id = request.form.get('department_id')
        if not name:
            flash('Name is required')
            return render_template('employees/edit.html', item=emp, departments=departments)
        if email:
            other = Employee.query.filter(Employee.email == email, Employee.id != emp.id).first()
            if other:
                flash('Email already taken')
                return render_template('employees/edit.html', item=emp, departments=departments)
        dep = Department.query.get(department_id) if department_id else None
        emp.name = name
        emp.email = email or None
        emp.department = dep
        db.session.commit()
        return redirect(url_for('employees.list_employees'))
    return render_template('employees/edit.html', item=emp, departments=departments)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_employee(id):
    emp = Employee.query.get_or_404(id)
    db.session.delete(emp)
    db.session.commit()
    return redirect(url_for('employees.list_employees'))