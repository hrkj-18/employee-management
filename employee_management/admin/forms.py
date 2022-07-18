from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_login import current_user

from employee_management.models import Employee, Role

class CreateEmployeeForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')


class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    role_id = IntegerField('Role ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_role_id(self, field):
        input_role_id = field.data
        existing_role_id = Role.query.filter_by(role_id=input_role_id).first()
        if existing_role_id and input_role_id!=current_user.role_id:
            raise ValidationError('Role ID is already in use.')


class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign Manager and role to employees
    """
    manager = QuerySelectField(query_factory=lambda: Employee.query.all(), get_label="email")
    role = QuerySelectField(query_factory=lambda: Role.query.all(), get_label="name")
    submit = SubmitField('Submit')
