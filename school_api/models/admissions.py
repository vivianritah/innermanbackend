from datetime import datetime
from school_api.extensions import db

class Admissions(db.Model):
    __tablename__ = "admissions"
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False, unique=True)
    tuition_day = db.Column(db.String(50))
    tuition_boarding = db.Column(db.String(50))
    registration_fees = db.Column(db.String(50), nullable=False)
    uniform_boarding = db.Column(db.String(50))
    uniform_day = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    def __init__(self, class_name, tuition_day=None, tuition_boarding=None,
                 registration_fees=None, uniform_boarding=None, uniform_day=None):
        self.class_name = class_name
        self.tuition_day = tuition_day
        self.tuition_boarding = tuition_boarding
        self.registration_fees = registration_fees
        self.uniform_boarding = uniform_boarding
        self.uniform_day = uniform_day
