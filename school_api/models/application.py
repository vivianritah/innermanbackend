from datetime import datetime
from school_api.extensions import db

class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    # event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    other_name = db.Column(db.String(50), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    name_of_previous_school = db.Column(db.String(100), nullable=False)
    previous_math_grade = db.Column(db.Integer, nullable=False)
    previous_english_grade = db.Column(db.Integer, nullable=False)
    current_level = db.Column(db.String(30), nullable=False)
    year_of_admission = db.Column(db.Integer, nullable=False)
    guardian_full_name = db.Column(db.String(70), nullable=True)
    guardian_contact = db.Column(db.String(15), nullable=True)
    guardian_email = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # event = db.relationship('Event', back_populates='applications', foreign_keys=[event_id])
    user = db.relationship('User', back_populates='applications', foreign_keys=[user_id])

    def __repr__(self):
        return f'<Application {self.first_name} {self.last_name}>'

    
    
    