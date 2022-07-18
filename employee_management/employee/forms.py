from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import current_user

from ..models import Employee


class EditEmployeeForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_number = IntegerField('Phone Number')
    submit = SubmitField('Submit')

    def validate_email(self, field):
        input_email = field.data
        existing_email = Employee.query.filter_by(email=input_email).first()
        if existing_email and input_email!=current_user.email:
            raise ValidationError('Email is already in use.')
