from App.models.student import Student  
from App.database import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError # Good practice for robust error handling

class StudentController:

    @staticmethod
    def create_student(name):
        if not name or len(str(name).strip()) == 0:
            return {"error": "Student name cannot be empty."}, 400
        
        name = str(name).strip()

        if Student.query.filter_by(name=name).first():
             return {"error": f"Student with name '{name}' already exists."}, 409 # 409 Conflict

        try:
            student = Student(name=name)
            db.session.add(student)
            db.session.commit()
            return student, 201 
        
        except (IntegrityError, SQLAlchemyError) as e:
            db.session.rollback()
            print(f"Database error during student creation: {e}") 
            return {"error": "An unexpected error occurred while saving the student."}, 500


    @staticmethod
    def get_all_students():
        """
        Retrieves all students.
        """
        students = Student.query.all()
        # Return list of model objects and 200 OK (even if list is empty)
        return students, 200 


    @staticmethod
    def get_student_by_id(studentID):
        """
        Retrieves a single student by ID.
        """
        # 1. Input Validation (ensure ID is usable)
        try:
            student_id = int(studentID)
        except (ValueError, TypeError):
            return {"error": "Invalid student ID format."}, 400

        # 2. Database Lookup
        student = Student.query.get(student_id)
        
        # 3. Determine Response
        if student:
            return student, 200 # Found, return model object and 200 OK
        else:
            return {"error": f"Student with ID {student_id} not found."}, 404 # 404 Not Found

    @staticmethod
    def login_student(name):
        student = Student.query.filter_by(name=name).first()
        if student :
            token = create_access_token(identity=name)
            response = jsonify(access_token=token)
            set_access_cookies(response, token)
            return response
        return {"Invalid username or password"}, 401
