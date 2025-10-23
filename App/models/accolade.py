from App.database import db

#student_accolade = db.Table('student_accolade', 
  # Link to the Student's primary key
  #  db.Column('studentID', db.Integer, db.ForeignKey('student.studentID'), primary_key=True),
    # Link to the Accolade's primary key
   # db.Column('accoladeID', db.Integer, db.ForeignKey('accolade.accoladeID'), primary_key=True)
#)


class Accolade(db.Model):
    accoladeID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.String(255))
    hoursNeeded = db.Column(db.Integer, nullable=False)

    def __init__(self, title, description, hoursNeeded):
        self.title = title
        self.description = description
        self.hoursNeeded = hoursNeeded

    def to_dict(self):
        return {
            'accoladeID': self.accoladeID,
            'title': self.title,
            'description': self.description,
            'hoursNeeded': self.hoursNeeded
        }

