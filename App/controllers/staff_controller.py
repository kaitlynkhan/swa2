from App.models.staff import Staff  
from App.models.hours_recorded import HoursRecorded
from App.database import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError 
from flask import jsonify
from flask_jwt_extended import create_access_token, set_access_cookies

class StaffController:

    @staticmethod
    def create_staff(name):
        if not name or len(str(name).strip()) == 0:
            return {"error": "Staff name cannot be empty."}, 400
        
        name = str(name).strip()

        if Staff.query.filter_by(name=name).first():
             return {"error": f"Staff with name '{name}' already exists."}, 409 # 409 Conflict

        try:
            staff = Staff(name=name)  
            db.session.add(staff)
            db.session.commit()
            return staff, 201 

        except (IntegrityError, SQLAlchemyError) as e:
            db.session.rollback()
            print(f"Database error during staff creation: {e}") 
            return {"error": "An unexpected error occurred while saving the staff."}, 500


    @staticmethod
    def confirm_hours(record_id, staff_id):
        try:
            record_id = int(record_id)
            staff_id = int(staff_id)
        except (ValueError, TypeError):
            return {"error": "Invalid ID format provided."}, 400

        staff = Staff.query.get(staff_id)  
        if not staff:
            return {"error": f"Staff member with ID {staff_id} not found."}, 404

        record = HoursRecorded.query.get(record_id)
        if not record:
            return {"error": f"Hours record with ID {record_id} not found."}, 404
        
        if record.confirmed:
            return {"message": f"Hours record ID {record_id} was already confirmed by Staff ID {record.staffID}."}, 400
    
        if not record.student:
            return {"error": f"Hours record ID {record_id} is not linked to any student."}, 400

        try:
            record.confirmed = True
            record.staffID = staff_id 
            record.student.totalHours += record.amount
            
            db.session.commit()

            return {
                "message": f"Hours record {record_id} confirmed by staff {staff_id}.",
                "record_id": record_id,
                "staff_name": staff.name,
                "student_id": record.student.id,
                "hours_added": record.amount
            }, 200 
            
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error during hour confirmation: {e}") 
            return {"error": "An unexpected error occurred during hour confirmation."}, 500

    @staticmethod
    def login_staff(name, password):
        staff = Staff.query.filter_by(name=name).first()
        if staff and staff.check_password(password):
            token = create_access_token(identity=name)
            response = jsonify(access_token=token)
            set_access_cookies(response, token)
            return response
        return jsonify(message="Invalid STAFFID"), 401
    
    
# Module-level wrapper functions for package-style imports
def create_staff(name):
    return StaffController.create_staff(name)

def confirm_hours(record_id, staff_id):
    return StaffController.confirm_hours(record_id, staff_id)

def login_staff(name, password):
    return StaffController.login_staff(name, password)

