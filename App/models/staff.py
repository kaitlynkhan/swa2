from App.database import db

class Staff(db.Model):
    staffID = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(120), nullable=False, unique=True) 
    
    # The 'HoursRecorded' model uses 'staffID' as the ForeignKey
    confirmedHours = db.relationship('HoursRecorded', backref='staff', lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Staff {self.staffID}: {self.name}>'
    
    def to_dict(self):
        return {
            'staffID': self.staffID,
            'name': self.name,
            'confirmedHoursCount': len(self.confirmedHours)
        }

