from flask import (
    render_template, 
    request, 
    Response, 
    flash, 
    redirect, 
    url_for, 
    jsonify
)
from flask_cors import cross_origin
import sys

from auth import auth as auth
from common import app, db, migrate, auth0
from models import Volunteer, Student, Classroom
from exceptions import APIException, GenericException
import util as util


@app.route('/')
@app.route('/home')
def index():
    return jsonify({"text": 'Welcome!', "success": True}), 200

@app.route('/volunteers')
@auth.requires_auth("get:volunteers")
def get_volunteers():
    try:
        volunteers = util.query_model(model=Volunteer, id=None)
        volunteers_list = [volunteer.short() for volunteer in volunteers]
        response = {
            "count": len(volunteers),
            "volunteers": volunteers_list
        }
        
        return jsonify(response), 200

    except GenericException as e:
        raise e

    except Exception:
        raise APIException("Internal Error", 500)


@app.route('/students')
@auth.requires_auth("get:students")
def get_students():
    try:
        students = util.query_model(model=Student, id=None)
        students_list = [student.short() for student in students]
        response = {
            "count": len(students),
            "volunteers": students_list
        }
        return jsonify(response), 200
    
    except GenericException as e:
        raise e

    except Exception:
        raise APIException("Internal Error", 500)


@app.route('/volunteer/<int:volunteer_id>')
@auth.requires_auth("get:volunteers")
def get_one_volunteer_info(volunteer_id):
    try:
        volunteer = util.query_model(model=Volunteer, id=volunteer_id)
        return jsonify(volunteer.long()), 200
    
    except GenericException as e:
        raise e

    except Exception:
        raise APIException("Internal Error", 500)


@app.route('/student/<int:student_id>')
@auth.requires_auth("get:students")
def get_one_student_info(student_id):
    try:
        student = util.query_model(model=Student, id=student_id)
        return jsonify(student.long()), 200
    
    except GenericException as e:
        raise e

    except Exception:
        raise APIException("Internal Error", 500)


@app.route('/classroom/<int:classroom_id>')
@auth.requires_auth("get:classrooms")
def get_one_classroom_info(classroom_id):
    try:
        classroom = util.query_model(model=Classroom, id=classroom_id)
        return jsonify(classroom.long()), 200
    
    except GenericException as e:
        raise e

    except Exception:
        raise APIException("Internal Error", 500)


@app.route('/volunteer/<int:volunteer_id>/classrooms')
@auth.requires_auth("get:classrooms")
def get_classrooms_of_one_volunteer(volunteer_id):
    try:
        volunteer = util.query_model(model=Volunteer, id=volunteer_id)

        classrooms = (db.session
            .query(Classroom, Student.name)
            .filter_by(volunteer_id=volunteer_id)
            .join(Student, Classroom.student_id == Student.id)
            .order_by(Classroom.id)
            .all())

        if not classrooms:
            raise APIException("Resource Not Found", 404)

        classroom_info_list = [{**classroom.long(), **{"student_name": student_name}} 
                               for classroom, student_name in classrooms]
        
        response = {
            "volunteer_id": volunteer_id,
            "volunteer_name": volunteer.name,
            "count": len(classrooms),
            "classrooms": classroom_info_list
        }

        return jsonify(response), 200

    except GenericException as e:
        raise e

    except Exception:
        raise APIException("Internal Error", 500)


@app.route('/student/<int:student_id>/classrooms')
@auth.requires_auth("get:classrooms")
def get_classrooms_of_one_student(student_id):
    try:
        student = util.query_model(model=Student, id=student_id)

        classrooms = (db.session
            .query(Classroom, Volunteer.name)
            .filter_by(student_id=student_id)
            .join(Volunteer, Classroom.volunteer_id == Volunteer.id)
            .order_by(Classroom.id)
            .all())

        if not classrooms:
            raise APIException("Resource Not Found", 404)    
    
        classroom_info_list = [{**classroom.long(), **{"volunteer_name": volunteer_name}} 
                               for classroom, volunteer_name in classrooms]
        
        response = {
            "student_id": student_id,
            "student_name": student.name,
            "count": len(classrooms),
            "classrooms": classroom_info_list
        }
        
        return jsonify(response), 200
    
    except GenericException as e:
        raise e

    except Exception:
        raise APIException("Internal Error", 500)


@app.route('/volunteer/register', methods=['POST'])
@auth.requires_auth("post:volunteer")
def register_volunteer():
    try:
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
    
    except GenericException as e:
        raise e

    except Exception:
        raise APIException("Bad Request", 400)


@app.route('/student/register', methods=['POST'])
@auth.requires_auth("post:student")
def register_student():
    try:
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
    
    except GenericException as e:
        raise e

    except Exception:
        raise APIException("Bad Request", 400)


@app.route('/classroom/create', methods=['POST'])
@auth.requires_auth("post:classroom")
def create_classroom():
    try:
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

    except GenericException as e:
        raise e

    except Exception:
        raise APIException("Bad Request", 400)


@app.route('/volunteer/<int:volunteer_id>', methods=['PATCH'])
@auth.requires_auth("patch:volunteer")
def edit_volunteer(volunteer_id):
    try:
        body = request.get_json()

        volunteer = util.query_model(model=Volunteer, id=volunteer_id)

        if 'name' in body:
            volunteer.name = body['name']
        if 'age' in body:
            volunteer.age = util.compute_int(body['age'])
        if 'gender' in body:
            volunteer.gender = body['gender']
        if 'image_link' in body:
            volunteer.image_link = body['image_link']
        if 'profile_link' in body:
            volunteer.profile_link = body['profile_link']
        if 'seeking_student' in body:
            volunteer.seeking_student = util.compute_boolean(body['seeking_student'])
        if 'seeking_description' in body:
            volunteer.seeking_description=body['seeking_description']
        
        volunteer.update()

        return jsonify({
            "success": True
            }), 200

    except GenericException as e:
        raise e

    except Exception as e:
        raise APIException("Bad Request", 400)


@app.route('/student/<int:student_id>', methods=['PATCH'])
@auth.requires_auth("patch:student")
def edit_student(student_id):
    try:
        body = request.get_json()

        student = util.query_model(model=Student, id=student_id)

        if 'name' in body:
            student.name = body['name']
        if 'age' in body:
            student.age = util.compute_int(body['age'])
        if 'gender' in body:
            student.gender = body['gender']
        if 'image_link' in body:
            student.image_link = body['image_link']
        if 'profile_link' in body:
            student.profile_link = body['profile_link']
        if 'seeking_volunteer' in body:
            student.seeking_volunteer = util.compute_boolean(body['seeking_volunteer'])
        if 'seeking_description' in body:
            student.seeking_description=body['seeking_description']
        
        student.update()

        return jsonify({
            "success": True
            }), 200

    except GenericException as e:
        raise e

    except Exception:
        raise APIException("Bad Request", 400)


@app.route('/classroom/<int:classroom_id>', methods=['PATCH'])
@auth.requires_auth("patch:classroom")
def edit_classroom(classroom_id):
    try:
        body = request.get_json()

        classroom = util.query_model(model=Classroom, id=classroom_id)

        if 'description' in body:
            classroom.description = body['description']
        if 'time' in body:
            classroom.time = body['time']
        if 'start_date' in body:
            classroom.start_date = body['start_date']
        if 'end_date' in body:
            classroom.end_date = body['end_date']

        classroom.update()

        return jsonify({
            "success": True
            }), 200

    except GenericException as e:
        raise e

    except Exception:
        raise APIException("Bad Request", 400)


@app.route('/volunteer/<int:volunteer_id>', methods=['DELETE'])
@auth.requires_auth("delete:volunteer")
def remove_volunteer(volunteer_id):
    try:
        volunteer = util.query_model(model=Volunteer, id=volunteer_id)
        volunteer.delete()

        return jsonify({
            "success": True
            }), 200

    except GenericException as e:
        raise e

    except Exception:
        raise APIException("Internal Error", 500)


@app.route('/student/<int:student_id>', methods=['DELETE'])
@auth.requires_auth("delete:student")
def remove_student(student_id):
    try:
        student = util.query_model(model=Student, id=student_id)
        student.delete()

        return jsonify({
            "success": True
            }), 200

    except GenericException as e:
        raise e

    except Exception:
        raise APIException("Internal Error", 500)


@app.route('/classroom/<int:classroom_id>', methods=['DELETE'])
@auth.requires_auth("delete:classroom")
def remove_classroom(classroom_id):
    try:
        classroom = util.query_model(model=Classroom, id=classroom_id)
        classroom.delete()
        
        return jsonify({
            "success": True
            }), 200

    except GenericException as e:
        raise e

    except Exception:
        raise APIException("Internal Error", 500)


@app.route('/volunteers/search', methods=['POST'])
@auth.requires_auth("get:volunteers")
def search_volunteer():
    """ Search for pattern match in name and seeking_description"""
    try:
        search_term = request.get_json().get('search_term', '')
        matching_volunteers = util.search_by_name_pattern(model=Volunteer, search_term=search_term)
        matching_volunteers_info = [volunteer.long() for volunteer in matching_volunteers]

        response = {
            "search_term": search_term,
            "count": len(matching_volunteers),
            "volunteers": matching_volunteers_info
        }
        
        return jsonify(response), 200

    except GenericException as e:
        raise e

    except Exception:
        print(sys.exc_info())
        raise APIException("Internal Error", 500)


@app.route('/students/search', methods=['POST'])
@auth.requires_auth("get:students")
def search_student():
    """ Search for pattern match in name and seeking_description"""
    try:
        search_term = request.get_json().get('search_term', '')
        matching_students = util.search_by_name_pattern(model=Student, search_term=search_term)
        matching_students_info = [student.long() for student in matching_students]

        response = {
            "search_term": search_term,
            "count": len(matching_students),
            "students": matching_students_info
        }
        
        return jsonify(response), 200

    except GenericException as e:
        raise e

    except Exception:
        raise APIException("Internal Error", 500)


@app.errorhandler(GenericException)
def api_errors(e):
    return jsonify({
                    "success": False, 
                    "error": e.status_code,
                    "message": e.error
                    }), e.status_code


if __name__ == '__main__':
    app.run(port=8002, debug=True)
