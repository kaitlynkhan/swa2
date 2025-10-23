import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.models import Student
from App.models import Staff
from App.main import create_app
from App.controllers import (create_user,create_staff, get_all_users_json, get_all_users, initialize)


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    jack = Student(name='Jack')
    jill = Student(name='Jill')
    mick = Staff(name='Mick')
    db.session.add_all([jack, jill, mick])
    db.session.commit()
    #stu = Student.query.all()
    #staff = Staff.query.all()
    #stu = get_all_students()
    print('database intialized')
    print("this is students " + str(stu))
    #print("this is staff " + str(staff))

@app.cli.command("createstaff", help="Creates and initializes the database")
def create_user_action():
    #data = request.get_json()
    name="kilddgdgde"

    staff, status = create_staff(name)
    print(str(staff) + str(status))

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)