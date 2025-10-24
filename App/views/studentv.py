from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user


from App.controllers.student_controller import StudentController
from App.controllers import unset_jwt_cookies

student_views = Blueprint('student_views', __name__, template_folder='../templates')


@student_views.route('/studentlogin/<name>', methods=['POST'])
def student_login_paage(name):
  response = login_student(name)
  if not response:
    return jsonify(message='bad username or password given'), 403
  return response

@student_views.route('/newstudent', methods=['POST'])
def create_user_action():
    data = request.get_json()
    student_name = data.get("name")
    student, status = create_student(student_name)
    return jsonify(student), status


@student_views.route('/<students>/accolades', methods=['POST'])
@jwt_required()
def get_student_accoldaes_page(studentID):
 student = get_student_by_id(studentID)#function to add
 accolades = student.get_student_accolades(studentID)
 return jsonify(accolades)


@student_views.route('/students/leaderboard', methods=['GET'])
def get_leaderboard_page():
   students = get_all_students()#function to add
   students.sort(key = students.totalHours)
   return students


@student_views.route('/<student>/reqHours', methods=['POST'])
@jwt_required()
def request_hours_page(staffID,studentID,hours):
    response = add_student_hours(studentID,staffID,hours)
    return response

@student_views.route('/studentlogout', methods=['GET'])
def logout():
  response = jsonify(message='Logged out')
  unset_jwt_cookies(response)
  return response