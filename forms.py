from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, FloatField, DateField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
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
    vehicle_id = SelectField('Assign Vehicle', coerce=int, choices=[(0, 'None')])
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
    insurance_expiry = DateField('Insurance Expiry', format='%Y-%m-%d', validators=[Optional()])
    status = SelectField('Status', choices=[('active','Active'), ('under_repair','Under Repair'), ('retired','Retired')])
    submit = SubmitField('Save')

class PaymentForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    type = SelectField('Type', choices=[('trip','Per Trip'), ('salary','Salary'), ('bonus','Bonus')])
    description = TextAreaField('Description')
    task_id = SelectField('Associated Task', coerce=int, choices=[(0, 'None')])
    submit = SubmitField('Record Payment')

class InvoiceForm(FlaskForm):
    client_name = StringField('Client Name', validators=[DataRequired()])
    client_email = StringField('Client Email')
    tasks = SelectMultipleField('Tasks', coerce=int)
    submit = SubmitField('Create Invoice')

class AdminUserEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('admin','Admin'), ('staff','Staff')])
    password = PasswordField('Password (leave blank to keep unchanged)')
    submit = SubmitField('Save')

# ------------------------------
# Partner Forms
# ------------------------------
class PartnerForm(FlaskForm):
    # Business Information
    business_name = StringField('Business Name', validators=[DataRequired()])
    business_type = SelectField('Business Type', choices=[
        ('limited_company', 'Limited Company'),
        ('registered_business', 'Registered Business'),
        ('sole_proprietorship', 'Sole Proprietorship')
    ], validators=[DataRequired()])
    registration_number = StringField('Registration Number', validators=[Optional()])
    kra_pin = StringField('KRA PIN', validators=[DataRequired(), Length(min=11, max=11)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    physical_address = StringField('Physical Address', validators=[Optional()])
    
    # Director Information
    director_name = StringField('Director/Proprietor Name', validators=[DataRequired()])
    director_id_number = StringField('Director ID Number', validators=[DataRequired()])
    director_phone = StringField('Director Phone', validators=[Optional()])
    director_email = StringField('Director Email', validators=[Optional(), Email()])
    
    # Documents - All required for onboarding
    git_cover = FileField('GIT Cover Document', validators=[FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'PDF and images only')])
    incorporation_cert = FileField('Certificate of Incorporation / Registration Cert / ID', validators=[FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'PDF and images only')])
    kra_certificate = FileField('KRA PIN Certificate', validators=[FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'PDF and images only')])
    logbook_copy = FileField('Copy of Logbooks', validators=[FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'PDF and images only')])
    director_id_copy = FileField("Copy of Director's ID", validators=[FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'PDF and images only')])
    driver_licenses = FileField('Driver Licenses (Select multiple if needed)', validators=[FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'PDF and images only')])
    contracts = FileField('Contracts (Select multiple if needed)', validators=[FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'PDF and images only')])
    
    # Fleet Details (Optional)
    vehicle_make = StringField('Vehicle Make', validators=[Optional()])
    vehicle_model = StringField('Vehicle Model', validators=[Optional()])
    vehicle_plate = StringField('Vehicle Plate Number', validators=[Optional()])
    vehicle_capacity_kg = FloatField('Vehicle Capacity (kg)', validators=[Optional()])
    
    submit = SubmitField('Register Partner')

class PartnerApprovalForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('approved', 'Approve'),
        ('rejected', 'Reject'),
        ('suspended', 'Suspend')
    ], validators=[DataRequired()])
    rejection_reason = TextAreaField('Reason (if rejecting or suspending)', validators=[Optional()])
    submit = SubmitField('Update Status')

class PartnerSearchForm(FlaskForm):
    business_name = StringField('Business Name', validators=[Optional()])
    kra_pin = StringField('KRA PIN', validators=[Optional()])
    status = SelectField('Status', choices=[
        ('', 'All'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended')
    ], validators=[Optional()])
    submit = SubmitField('Search')