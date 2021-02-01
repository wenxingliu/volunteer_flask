from flask import render_template, request, Response, flash, redirect, url_for, jsonify

from common import app, db, migrate
from models import Volunteer, Student, Classroom
import util as util


@app.route('/')
@app.route('/home')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Volunteer-Home', user=user)


@app.route('/volunteers')
def get_volunteers():
    volunteers = Volunteer.query.order_by('id').all()
    volunteers_list = [volunteer.short() for volunteer in volunteers]
    response = {
        "count": len(volunteers),
        "volunteers": volunteers_list
    }
    return jsonify(response), 200


@app.route('/students')
def get_students():
    students = Student.query.order_by('id').all()
    students_list = [student.short() for student in students]
    response = {
        "count": len(students),
        "volunteers": students_list
    }
    return jsonify(response), 200


@app.route('/volunteer/<int:volunteer_id>')
def get_one_volunteer_info(volunteer_id):
    volunteer = Volunteer.query.get(volunteer_id)
    return jsonify(volunteer.long()), 200


@app.route('/student/<int:student_id>')
def get_one_student_info(student_id):
    student = Student.query.get(student_id)
    return jsonify(student.long()), 200


@app.route('/volunteer/<int:volunteer_id>/classrooms')
def get_classrooms_of_one_volunteer(volunteer_id):
    volunteer = Volunteer.query.get(volunteer_id)

    classrooms = (db.session
        .query(Classroom, Student.name)
        .filter_by(volunteer_id=volunteer_id)
        .join(Student, Classroom.student_id == Student.id)
        .order_by(Classroom.id)
        .all())
    
    classroom_info_list = [{**classroom.short(), **{"student_name": student_name}} 
                           for classroom, student_name in classrooms]
    
    response = {
        "volunteer_id": volunteer_id,
        "volunteer_name": volunteer.name,
        "count": len(classrooms),
        "classrooms": classroom_info_list
    }

    return jsonify(response), 200


@app.route('/student/<int:student_id>/classrooms')
def get_classrooms_of_one_student(student_id):
    student = Student.query.get(student_id)

    classrooms = (db.session
        .query(Classroom, Volunteer.name)
        .filter_by(student_id=student_id)
        .join(Volunteer, Classroom.volunteer_id == Volunteer.id)
        .order_by(Classroom.id)
        .all())
    
    classroom_info_list = [{**classroom.short(), **{"volunteer_name": volunteer_name}} 
                           for classroom, volunteer_name in classrooms]
    
    response = {
        "student_id": student_id,
        "student_name": student.name,
        "count": len(classrooms),
        "classrooms": classroom_info_list
    }
    
    return jsonify(response), 200


@app.route('/volunteer/register', methods=['POST'])
def register_volunteer():
    body = request.get_json()
    volunteer = Volunteer(
        name=body['name'],
        age=util.compute_int(body['age']),
        gender=body.get('gender', 'NA'),
        email=body['email'],
        image_link=body.get('image_link', ''),
        profile_link=util.compute_profile_link(),
        seeking_student=util.compute_boolean(body['seeking_student']),
        seeking_description=body['seeking_description']
    )

    volunteer.insert()

    return jsonify({
        "success": True
        }), 200


@app.route('/student/register', methods=['POST'])
def register_student():
    body = request.get_json()
    student = Student(
        name=body['name'],
        age=util.compute_int(body['age']),
        gender=body.get('gender', 'NA'),
        email=body['email'],
        image_link=body.get('image_link', ''),
        profile_link=util.compute_profile_link(),
        seeking_volunteer=util.compute_boolean(body['seeking_volunteer']),
        seeking_description=body['seeking_description']
    )

    student.insert()

    return jsonify({
        "success": True
        }), 200


@app.route('/classroom/create', methods=['POST'])
def create_classroom():
    body = request.get_json()
    classroom = Classroom(
        description=body['description'],
        time = body['time'],
        start_date = body['start_date'],
        end_date = body.get('end_date'),
        volunteer_id = body['volunteer_id'],
        student_id = body['student_id']
    )

    classroom.insert()

    return jsonify({
        "success": True
        }), 200


if __name__ == '__main__':
    app.run(port=8002, debug=True)
