from App.models.student import Student # Assuming explicit import from App.models 
from App.models.hours_recorded import HoursRecorded
from App.database import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError 

class HoursController:

    @staticmethod
    def add_student_hours(student_id: int, staff_id: int, amount: int):
       
        try:
            student_id = int(student_id)
            staff_id = int(staff_id)
            amount = int(amount)
        except (ValueError, TypeError):
            return {"error": "Invalid ID or amount format provided."}, 400

        if amount <= 0:
            return {"error": "Hours amount must be positive."}, 400

        student = Student.query.get(student_id)    
        if not student:
            return {"error": f"Student ID {student_id} not found."}, 404

        try:
            new_hours_record = HoursRecorded (
                studentID=student_id,
                staffID=staff_id,
                amount=amount,
                confirmed=False  
            )
            db.session.add(new_hours_record)
            db.session.commit()
           
            return {
                "message": f"Added {amount} hours for Student {student_id}. Pending staff confirmation.",
                "record_id": new_hours_record.id,
                "student_name": student.name,
                "amount": amount
            }, 201 

        except (IntegrityError, SQLAlchemyError) as e:
            db.session.rollback()
            print(f"Database error during hours addition: {e}") 
            return {"error": "An unexpected database error occurred while adding hours."}, 500


    @staticmethod
    def confirm_student_hours(hour_id: int):
        try:
            hour_id = int(hour_id)
        except (ValueError, TypeError):
            return {"error": "Invalid hours record ID format."}, 400

        record = HoursRecorded.query.get(hour_id)
        if not record:
            return {"error": f"Hours record ID {hour_id} not found."}, 404
        
        if record.confirmed:
            return {"message": f"Record ID {hour_id} already confirmed."}, 400 # 400 Bad Request
        
             #return {"error": f"Record ID {hour_id} is not linked to any student."}, 400

        try:
            record.confirmed = True
            record.student.hours_completed += record.amount

            db.session.commit()
            
            return {
                "message": f"Confirmed {record.amount} hours for Student {record.studentID}.",
                "record_id": record.id
            }, 200 

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error during hour confirmation: {e}") 
            return {"error": "An unexpected database error occurred during confirmation."}, 500

    @staticmethod
    def get_hours_by_id(hour_id: int):
        try:
            hour_id = int(hour_id)
        except (ValueError, TypeError):
            return {"error": "Invalid hours record ID format."}, 400

        record = HoursRecorded.query.get(hour_id)
        
        if not record:
            return {"error": f"Hours record ID {hour_id} not found."}, 404
        
        return record, 200 


# Module-level wrappers
def add_student_hours(student_id, staff_id, amount):
    return HoursController.add_student_hours(student_id, staff_id, amount)

def confirm_student_hours(hour_id):
    return HoursController.confirm_student_hours(hour_id)

def get_hours_by_id(hour_id):
    return HoursController.get_hours_by_id(hour_id)