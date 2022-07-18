from . import admin
from flask import current_app, flash, render_template, abort, redirect, url_for
from flask_login import current_user, login_required

from employee_management.models import Employee, Role
from .forms import CreateEmployeeForm, RoleForm, EmployeeAssignForm

from employee_management import db


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


@admin.route('/roles')
def list_roles():
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(
            role_id=form.role_id.data,
            name=form.name.data,
            description=form.description.data
        )

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.role_id = form.role_id.data
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))
    form.role_id.data = role.role_id
    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))


@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')

@admin.route('/employees/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    """
    Add a employee to the database
    """
    check_admin()

    add_employee = True

    form = CreateEmployeeForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        try:
            # add role to the database
            db.session.add(employee)
            db.session.commit()
            flash('You have successfully added a new employee.')
        except:
            # in case role name already exists
            flash('Error: employee already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    # load role template
    return render_template('admin/employees/edit_employee.html', add_employee=add_employee,
                           form=form, title='Add Employee')


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a manager and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a manager or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.manager = form.manager.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a manager and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/edit_employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')


@admin.route('/employee/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    """
    Delete an employee from the database
    """
    check_admin()

    if current_user.id == id:
        abort(403)

    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('You have successfully deleted the employee.')

    # redirect to the roles page
    return redirect(url_for('admin.list_employees'))
