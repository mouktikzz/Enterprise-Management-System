from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page')
            return redirect(url_for('auth.login'))
        if current_user.role != 'admin':
            flash('Admin access required')
            abort(403)
        return fn(*args, **kwargs)
    return wrapper


def employee_or_admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page')
            return redirect(url_for('auth.login'))
        return fn(*args, **kwargs)
    return wrapper