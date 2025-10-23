from App.database import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

# Helper for the many-to-many relationship
student_accolade = db.Table('student_accolade',
    db.Column('studentID', db.Integer, db.ForeignKey('student.studentID'), primary_key=True),
    db.Column('accoladeID', db.Integer, db.ForeignKey('accolade.accoladeID'), primary_key=True)
)


class Student(db.Model):
    studentID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    totalHours = db.Column(db.Integer, default=0)

    hours = db.relationship('HoursRecorded', backref='student', lazy=True)
    accolades = db.relationship('Accolade',
                                secondary=student_accolade, 
                                backref=db.backref('students', lazy='dynamic'),
                                lazy='dynamic')
    
    def __init__(self, name):
        self.name = name 

    def __repr__(self):
        return f'<Student {self.studentID}: {self.name}>'

    def to_dict(self):
        """Converts the model object into a dictionary for API response."""
        accolade_list = []
        # Safely serialize accolades if loaded
        if self.accolades:
            accolade_list = [accolade.to_dict() for accolade in self.accolades.all()]

        return {
            'studentID': self.studentID,
            'name': self.name,
            'totalHours': self.totalHours,
            'accolades': accolade_list,
        }

