from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from App.controllers.student_controller import StudentController
from App.controllers import unset_jwt_cookies

student_views = Blueprint('student_views', __name__, template_folder='../templates')


@student_views.route('/studentlogin/<name>', methods=['POST'])
def student_login_page(name):
    response = StudentController.login_student(name)
    if not response:
        return jsonify(message='Bad username or password given'), 403
    return response


@student_views.route('/newstudent', methods=['POST'])
def create_user_action():
    data = request.get_json()
    student_name = data.get("name")

    student, status = StudentController.create_student(student_name)
    if isinstance(student, dict):  # handle error response
        return jsonify(student), status
    return jsonify({"id": student.id, "name": student.name}), status


@student_views.route('/<int:student_id>/accolades', methods=['GET'])
@jwt_required()
def get_student_accolades_page(student_id):
    student, status = StudentController.get_student_by_id(student_id)
    if isinstance(student, dict):
        return jsonify(student), status
    accolades = student.get_student_accolades() if hasattr(student, 'get_student_accolades') else []
    return jsonify(accolades), 200


@student_views.route('/students/leaderboard', methods=['GET'])
def get_leaderboard_page():
    students, status = StudentController.get_all_students()
    if isinstance(students, dict):
        return jsonify(students), status

    # Convert to JSON-safe format
    student_list = [{"id": s.id, "name": s.name, "hours": getattr(s, "totalHours", 0)} for s in students]
    student_list.sort(key=lambda x: x["hours"], reverse=True)
    return jsonify(student_list), 200


@student_views.route('/<int:student_id>/reqHours', methods=['POST'])
@jwt_required()
def request_hours_page(student_id):
    data = request.get_json()
    staff_id = data.get("staffID")
    hours = data.get("hours")

    # Assuming add_student_hours is implemented in your controllers
    try:
        from App.controllers.hours_controller import add_student_hours
        response = add_student_hours(student_id, staff_id, hours)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@student_views.route('/studentlogout', methods=['GET'])
def logout():
    response = jsonify(message='Logged out')
    unset_jwt_cookies(response)
    return response
