from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ------------------------------
# Company (for multi‑tenant)
# ------------------------------
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    users = db.relationship('User', backref='company', lazy=True)
    drivers = db.relationship('Driver', backref='company', lazy=True)
    vehicles = db.relationship('Vehicle', backref='company', lazy=True)
    tasks = db.relationship('Task', backref='company', lazy=True)
    invoices = db.relationship('Invoice', backref='company', lazy=True)

# ------------------------------
# User
# ------------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='staff')          # 'admin' or 'staff'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    # Relationships
    drivers = db.relationship('Driver', backref='user', lazy=True, cascade='all, delete-orphan')
    tasks = db.relationship('Task', backref='assigner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# ------------------------------
# Vehicle
# ------------------------------
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    plate = db.Column(db.String(20), unique=True, nullable=False)
    capacity_kg = db.Column(db.Float, nullable=True)
    insurance_expiry = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), default='active')   # active, under_repair, retired
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    # One‑to‑one with Driver (optional)
    driver = db.relationship('Driver', backref='vehicle', uselist=False)
    maintenance_records = db.relationship('MaintenanceRecord', backref='vehicle', lazy=True, cascade='all, delete-orphan')

# ------------------------------
# Driver (updated)
# ------------------------------
class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    certificate_of_conduct = db.Column(db.String(200))
    driving_license = db.Column(db.String(200))
    national_id = db.Column(db.String(200))
    car_number_plate = db.Column(db.String(20), unique=True, nullable=False)
    vehicle_picture = db.Column(db.String(200))
    phone = db.Column(db.String(20), nullable=False)
    passport_photo = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)   # optional

    tasks = db.relationship('Task', backref='driver', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='driver', lazy=True)

# ------------------------------
# Task (updated)
# ------------------------------
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    load_location = db.Column(db.String(200), nullable=False)
    offload_location = db.Column(db.String(200), nullable=False)
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    completed_date = db.Column(db.DateTime)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    # Route & distance fields
    distance_km = db.Column(db.Float, nullable=True)
    estimated_duration_sec = db.Column(db.Integer, nullable=True)
    fuel_cost = db.Column(db.Float, nullable=True)

    # Optional: store geometry as GeoJSON string
    # route_geometry = db.Column(db.Text, nullable=True)

# ------------------------------
# Payment
# ------------------------------
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(20), nullable=False)          # 'trip', 'salary', 'bonus'
    description = db.Column(db.Text, nullable=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=True)   # if per‑trip

    # Relationships
    task = db.relationship('Task', backref='payment')

# ------------------------------
# Invoice (and its many‑to‑many with Task)
# ------------------------------
invoice_task = db.Table('invoice_task',
    db.Column('invoice_id', db.Integer, db.ForeignKey('invoice.id')),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_email = db.Column(db.String(100), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Boolean, default=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    tasks = db.relationship('Task', secondary=invoice_task, backref='invoices')

# ------------------------------
# Maintenance Record
# ------------------------------
class MaintenanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Float, nullable=True)
    next_due = db.Column(db.Date, nullable=True)