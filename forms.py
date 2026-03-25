from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, FloatField, DateField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('staff', 'User'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class DriverForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    car_number_plate = StringField('Car Number Plate', validators=[DataRequired()])
    vehicle_id = SelectField('Assign Vehicle', coerce=int, choices=[(0, 'None')])  # added
    certificate_of_conduct = FileField('Certificate of Good Conduct', validators=[FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'PDF/Image only')])
    driving_license = FileField('Driving License', validators=[FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'PDF/Image only')])
    national_id = FileField('National ID', validators=[FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'PDF/Image only')])
    vehicle_picture = FileField('Vehicle Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only')])
    passport_photo = FileField('Passport Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only')])
    submit = SubmitField('Register Driver')

class TaskForm(FlaskForm):
    load_location = TextAreaField('Load Location', validators=[DataRequired()])
    offload_location = TextAreaField('Offload Location', validators=[DataRequired()])
    submit = SubmitField('Assign Task')

class SearchForm(FlaskForm):
    plate = StringField('Car Number Plate', validators=[DataRequired()])
    name = StringField('Driver Name')
    vehicle_status = SelectField('Vehicle Status', choices=[('', 'All'), ('active','Active'), ('under_repair','Under Repair'), ('retired','Retired')])
    expiry_soon = BooleanField('Insurance Expiring Soon')
    submit = SubmitField('Search')

# --------------------------
# New forms for added features
# --------------------------
class VehicleForm(FlaskForm):
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    plate = StringField('License Plate', validators=[DataRequired(), Length(max=20)])
    capacity_kg = FloatField('Capacity (kg)')
    insurance_expiry = DateField('Insurance Expiry', format='%Y-%m-%d')
    status = SelectField('Status', choices=[('active','Active'), ('under_repair','Under Repair'), ('retired','Retired')])
    submit = SubmitField('Save')

class PaymentForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    type = SelectField('Type', choices=[('trip','Per Trip'), ('salary','Salary'), ('bonus','Bonus')])
    description = TextAreaField('Description')
    task_id = SelectField('Associated Task', coerce=int, choices=[(0, 'None')])  # populated dynamically
    submit = SubmitField('Record Payment')

class InvoiceForm(FlaskForm):
    client_name = StringField('Client Name', validators=[DataRequired()])
    client_email = StringField('Client Email')
    tasks = SelectMultipleField('Tasks', coerce=int)  # populated dynamically
    submit = SubmitField('Create Invoice')

class AdminUserEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('admin','Admin'), ('staff','Staff')])
    password = PasswordField('Password (leave blank to keep unchanged)')
    submit = SubmitField('Save')