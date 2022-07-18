from flask import current_app, flash, redirect, render_template, url_for, abort
from flask_login import login_required, current_user

from . import employee
from ..models import Employee
from .forms import EditEmployeeForm
from employee_management import db


@employee.route('/employee/<int:id>')
@login_required
def view_profile(id):
    """
    List employee details
    """

    employee = Employee.query.get_or_404(id)
    return render_template(
        'admin/employees/employee.html',
        employee=employee,
        title=f'{employee.first_name}'
    )


@employee.route('/edit_details/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_details(id):
    """
    List employee details
    """
    if current_user.id != id:
        abort(403)

    employee = Employee.query.get_or_404(id)
    form = EditEmployeeForm(obj=employee)
    if form.validate_on_submit():
        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
        employee.email = form.email.data
        employee.phone_number = form.phone_number.data
        try:
            # add role to the database
            db.session.add(employee)
            db.session.commit()
            current_app.logger.debug(f'Details Edited of user: {employee.first_name}')
            flash('You have successfully edited your details.')
        except:
            # in case role name already exists
            current_app.logger.warning('Employee already exists')
            flash('Error: employee already exists.')

        return redirect(url_for('employee.view_profile', id=employee.id))

    form.first_name.data = employee.first_name
    form.last_name.data = employee.last_name
    form.email.data = employee.email
    form.phone_number.data = employee.phone_number
    return render_template(
        'admin/employees/edit_employee.html',
        employee=employee,
        edit_employee=True,
        form=form,
        title=f'{employee.first_name}'
    )