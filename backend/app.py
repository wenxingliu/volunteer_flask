from flask import render_template, request, Response, flash, redirect, url_for, jsonify

from common import app, db, migrate
from models import Volunteer, Student, Classroom
from exceptions import APIException, GenericException
import util as util


@app.route('/')
@app.route('/home')
def index():
    return 'Welcome!'


@app.route('/volunteers')
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

    except:
        raise APIException("Internal Error", 500)


@app.route('/volunteer/<int:volunteer_id>')
def get_one_volunteer_info(volunteer_id):
    try:
        volunteer = util.query_model(model=Volunteer, id=volunteer_id)
        return jsonify(volunteer.long()), 200
    
    except GenericException as e:
        raise e

    except:
        raise APIException("Internal Error", 500)


@app.route('/student/<int:student_id>')
def get_one_student_info(student_id):
    try:
        student = util.query_model(model=Student, id=student_id)
    
    except GenericException as e:
        raise e

    except:
        raise APIException("Internal Error", 500)


@app.route('/volunteer/<int:volunteer_id>/classrooms')
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

        classroom_info_list = [{**classroom.short(), **{"student_name": student_name}} 
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

    except:
        raise APIException("Internal Error", 500)


@app.route('/student/<int:student_id>/classrooms')
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
    
        classroom_info_list = [{**classroom.short(), **{"volunteer_name": volunteer_name}} 
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

    except:
        raise APIException("Internal Error", 500)


@app.route('/volunteer/register', methods=['POST'])
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

    except:
        raise APIException("Bad Request", 400)


@app.route('/student/register', methods=['POST'])
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

    except:
        raise APIException("Bad Request", 400)


@app.route('/classroom/create', methods=['POST'])
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

    except:
        raise APIException("Bad Request", 400)


@app.route('/volunteer/<int:volunteer_id>/edit', methods=['PATCH'])
def edit_volunteer(volunteer_id):
    try:
        body = request.get_json()

        volunteer = util.query_model(model=Volunteer, id=volunteer_id)
        volunteer.name = body['name']
        volunteer.age = util.compute_int(body['age'])
        volunteer.gender = body['gender']
        volunteer.image_link = body['image_link']
        volunteer.profile_link = body['profile_link']
        volunteer.seeking_student = util.compute_boolean(body['seeking_student'])
        volunteer.seeking_description=body['seeking_description']
        volunteer.update()

    except GenericException as e:
        raise e

    except:
        raise APIException("Bad Request", 400)


@app.route('/student/<int:student_id>/edit', methods=['PATCH'])
def edit_student(student_id):
    try:
        body = request.get_json()

        student = util.query_model(model=Student, id=student_id)
        student.name = body['name']
        student.age = util.compute_int(body['age'])
        student.gender = body['gender']
        student.image_link = body['image_link']
        student.profile_link = body['profile_link']
        student.seeking_volunteer = util.compute_boolean(body['seeking_volunteer'])
        student.seeking_description=body['seeking_description']
        student.update()

    except GenericException as e:
        raise e

    except:
        raise APIException("Bad Request", 400)


@app.route('/classroom/<int:classroom_id>/edit', methods=['PATCH'])
def edit_classroom(classroom_id):
    try:
        body = request.get_json()

        classroom = util.query_model(model=Classroom, id=classroom_id)
        classroom.description = body['description']
        classroom.time = body['time']
        classroom.start_date = body['start_date']
        classroom.end_date = body['end_date']
        classroom.update()

    except GenericException as e:
        raise e

    except:
        raise APIException("Bad Request", 400)


@app.route('/volunteers/search', methods=['POST'])
def search_volunteer():
    raise NotImplementedError


@app.route('/students/search', methods=['POST'])
def search_student():
    raise NotImplementedError


@app.route('/classrooms/search', methods=['POST'])
def search_classroom():
    raise NotImplementedError


@app.errorhandler(GenericException)
def api_errors(e):
    return jsonify({
                    "success": False, 
                    "error": e.status_code,
                    "message": e.error
                    }), e.status_code


if __name__ == '__main__':
    app.run(port=8002, debug=True)
