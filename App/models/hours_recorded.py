from App.database import db
from datetime import datetime

class HoursRecorded(db.Model):
    recordId = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255))
    confirmed = db.Column(db.Boolean, default=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_confirmed = db.Column(db.DateTime, nullable=True) 
    
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'), nullable=False)
    # staffID is nullable because it's only set AFTER confirmation
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'), nullable=True) 
    
    
    def __init__(self, studentID, amount, description=None):
        self.studentID = studentID
        self.amount = amount
        self.description = description
    
    def to_dict(self):
        """Converts the model object into a dictionary for API response."""
        return {
            'recordId': self.recordId,
            'studentID': self.studentID,
            'amount': self.amount,
            'description': self.description,
            'confirmed': self.confirmed,
            'staffID': self.staffID, 
            # Format dates using ISO 8601 for clean API consumption
            'date_submitted': self.date_submitted.isoformat() if self.date_submitted else None,
            'date_confirmed': self.date_confirmed.isoformat() if self.date_confirmed else None
        }

