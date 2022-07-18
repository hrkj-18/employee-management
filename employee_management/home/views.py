from flask import current_app, render_template, abort
from flask_login import login_required, current_user

from . import home


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    current_app.logger.debug('Homepage')
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    current_app.logger.debug('Dashboard')
    return render_template('home/dashboard.html', title="Dashboard")


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        current_app.logger.debug('Not a admin')
        abort(403)

    current_app.logger.debug('Admin Dashboard')
    return render_template('home/admin_dashboard.html', title="Dashboard")
