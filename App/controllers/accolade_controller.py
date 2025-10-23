from App.models.accolade import Accolade  
from App.models.student import Student
from App.database import db
from sqlalchemy.exc import SQLAlchemyError 

class AccoladeController:
    @staticmethod
    def award_accolade(student_id, accolade_id):
    
        try:
            student_id = int(student_id)
            accolade_id = int(accolade_id)
        except (ValueError, TypeError):
            return {"error": "Invalid ID format provided."}, 400

        student = Student.query.get(student_id)
        if not student:
            return {"error": f"Student ID {student_id} not found."}, 404

        accolade = Accolade.query.get(accolade_id)
        if not accolade:
            return {"error": f"Accolade ID {accolade_id} not found."}, 404

       
        if accolade in student.accolades:
            return {
                "message": f"Student {student_id} already has the accolade: {accolade.name if hasattr(accolade, 'name') else accolade_id}"
            }, 400 

        try:
            student.accolades.append(accolade)
            db.session.commit()

            return {
                "message": f"Successfully awarded accolade '{accolade.name}' to student {student_id}.",
                "student_id": student_id,
                "accolade_id": accolade_id
            }, 200 
            
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error during accolade award: {e}")
            return {"error": "An unexpected database error occurred while awarding the accolade."}, 500

    @staticmethod
    def create_accolade(name, description):
        if not name:
            return {"error": "Accolade name is required."}, 400

        try:
            accolade = Accolade(name=name, description=description)
            db.session.add(accolade)
            db.session.commit()
            return accolade, 201
        except SQLAlchemyError:
            db.session.rollback()
            return {"error": "Could not create accolade due to a database issue."}, 500
            
    @staticmethod
    def get_student_accolades(student_id):
        try:
            student_id = int(student_id)
        except (ValueError, TypeError):
            return {"error": "Invalid student ID format provided."}, 400

        student = Student.query.get(student_id)
        if not student:
            return {"error": f"Student ID {student_id} not found."}, 404
        
        return student.accolades, 200


# Module-level wrappers for package imports
def award_accolade(student_id, accolade_id):
    return AccoladeController.award_accolade(student_id, accolade_id)

def create_accolade(name, description):
    return AccoladeController.create_accolade(name, description)

def get_student_accolades(student_id):
    return AccoladeController.get_student_accolades(student_id)



