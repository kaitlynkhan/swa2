
from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from App.controllers import (
    create_staff,
    login_staff,
    unset_jwt_cookies,
    confirm_hours,
    confirm_student_hours
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/newstaff/<name>', methods=['POST'])
def create_staff_action(name):
  response,status= create_staff(name)
    return jsonify(response), status 


@staff_views.route('/login', methods=['POST'])
def staff_login_page(staffID,password):
  data = request.json
  response = login_staff(data['username'], data['password'])
  if not response:
    return jsonify(message='bad username or password given'), 403
  return response

@staff_views.route('/<staff>/confirm_hours', methods=['POST'], endpoint='confirm_hours_page')
@jwt_required()
def confirm_hours_page(recordID,staffID):
    response = confirm_hours(recordID, staffID)
    return response

@staff_views.route('/<staff>/change_hours', methods=['POST'], endpoint='change_hours_page')
@jwt_required()
def comfirm_hourrs_page(hour_id):
  response= confirm_student_hours(hour_id)
  return response

@staff_views.route('/stafflogout', methods=['GET'], endpoint='staff_logout')
@jwt_required()
def logout():
  response = jsonify(message='Logged out')
  unset_jwt_cookies(response)
  return response