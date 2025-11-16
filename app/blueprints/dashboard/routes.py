from flask import render_template
from . import bp
from ...models import User, Department, Employee


@bp.route('/')
def index():
    counts = {
        'users': User.query.count(),
        'departments': Department.query.count(),
        'employees': Employee.query.count(),
    }
    return render_template('dashboard/index.html', counts=counts)