from flask import current_app, flash, jsonify, render_template, abort
from flask_login import login_required, current_user

from . import home
from employee_management.models import Employee, Role


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")


@home.route('/get_employees')
def get_employees():
    current_app.logger.debug('This is a DEBUG message')
    employees = Employee.query.all()
    return jsonify('employees', employees)

# @home.route('/get_roles')
# def get_roles():
#     current_app.logger.debug('This is a DEBUG message')
#     roles = Role.query.all()
#     print({'roles':roles})
#     return {'roles':roles}




