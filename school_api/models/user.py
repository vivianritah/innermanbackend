# user.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from school_api.extensions import db, bcrypt

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)
    isadmin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    events = db.relationship('Event', back_populates='user', cascade="all, delete-orphan")
    applications = db.relationship('Application', back_populates='user', cascade="all, delete-orphan")

    def __init__(self, first_name, last_name, email, password, user_type='admin', isadmin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.user_type = user_type
        self.isadmin = isadmin

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
