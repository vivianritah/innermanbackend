# from datetime import datetime
# from school_api import db

# class Notification(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     message = db.Column(db.String(255), nullable=False)
#     user_id = db.Column(db.Integer, nullable=False)  # Assuming notifications are user-specific
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     is_read = db.Column(db.Boolean, default=False)
#     application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=True)

#     def __repr__(self):
#         return f"Notification('{self.message}', '{self.timestamp}')"


from datetime import datetime
from school_api.extensions import db

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)  # Assuming notifications are user-specific
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    applications_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=True)

    def __repr__(self):
        return f"Notification('{self.message}', '{self.timestamp}')"