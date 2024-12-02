# Data models
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from datetime import datetime
db = SQLAlchemy()

# Enum for roles
class UserRole(Enum):
    ADMIN = 0
    CUSTOMER = 1
    PROFESSIONAL = 2

#Enum for status
class ServiceRequestStatus(Enum):
    PENDING = 1
    ACCEPTED = 2
    COMPLETED = 3
    CANCELLED = 4




# User Entity (Parent Table)
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    customer_details = db.relationship("Customer", backref="user", uselist=False, lazy=True, cascade="all, delete") #user can access all of its customer details
    professional_details = db.relationship("Professional", backref="user", uselist=False, lazy=True, cascade="all, delete") #user can access all of its professional details

    def __repr__(self):
        return f"<User {self.full_name} ({self.role.name})>"

# Customer Entity (Child of User)
class Customer(db.Model):
    __tablename__ = "customer"

    customer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)

    # Relationships
    service_requests = db.relationship("ServiceRequest", backref="customer", lazy=True, cascade="all, delete") # customer can access its service requests

# Professional Entity (Child of User)
class Professional(db.Model):
    __tablename__ = "professional"

    professional_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("service.service_id"), nullable=False)
    experience = db.Column(db.Integer)
    description = db.Column(db.String(500))
    city = db.Column(db.String(100), nullable=False)
    is_occupied = db.Column(db.Boolean, default=False)
    document_path = db.Column(db.String(200), nullable=True)  # Path to the uploaded document
    is_approved = db.Column(db.Boolean, default=False)  # New field for approval status

    # Relationships
    service_requests = db.relationship("ServiceRequest", backref="professional", lazy=True, cascade="all, delete") # professional can access its service requests
    reviews = db.relationship("Review", backref="professional", lazy=True, cascade="all, delete") # professional can access its reviews

# Service Entity
class Service(db.Model):
    __tablename__ = "service"

    service_id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    min_price = db.Column(db.Integer, nullable=False)
    min_time_required = db.Column(db.Integer, nullable=False)  # Time in minutes

    # Relationships
    professionals = db.relationship("Professional", backref="service", lazy=True, cascade="all, delete") #service can access its professionals
    service_requests = db.relationship("ServiceRequest", backref="service", lazy=True, cascade="all, delete") #service can access its service requests

# Service Request Entity
class ServiceRequest(db.Model):
    __tablename__ = "service_request"

    service_request_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("service.service_id"), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional.professional_id"), nullable=False)
    service_request_time = db.Column(db.DateTime)
    status = db.Column(db.Enum(ServiceRequestStatus), default=ServiceRequestStatus.PENDING, nullable=False)

    # Relationships
    reviews = db.relationship("Review", backref="service_request", lazy=True, cascade="all, delete") # service_request  can access its reviews
    complaints = db.relationship("Complaint", backref="service_request", lazy=True, cascade="all, delete") # service_request can access its complaints

# Review Entity
class Review(db.Model):
    __tablename__ = "review"

    review_id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey("service_request.service_request_id"), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional.professional_id"), nullable=False)
    rating = db.Column(db.Integer, default=0)
    review = db.Column(db.String(500))

# Complaint Entity
class Complaint(db.Model):
    __tablename__ = "complaint"

    complaint_id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey("service_request.service_request_id"), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional.professional_id"), nullable=False)
    description = db.Column(db.String(500))






    

