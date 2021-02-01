import datetime as dt
from flask_wtf import Form
from wtforms.validators import DataRequired, AnyOf, URL
from wtforms import (
    StringField, 
    SelectField, 
    SelectMultipleField, 
    DateField, 
    TimeField,
    IntegerField
)


class ClassroomForm(Form):
    volunteer_id = StringField(
        'volunteer_id'
    )
    student_id = StringField(
        'student_id'
    )
    description = StringField(
        'description'
    )
    time = TimeField(
        'time',
        validators=[DataRequired()],
        default= dt.time(20, 0)
    )
    start_date = DateField(
        'start_date',
        validators=[DataRequired()],
        default= dt.datetime.today().date
    )
    end_date = DateField(
        'end_date',
        validators=[DataRequired()],
        default= dt.datetime.today().date
    )


class VolunteerForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    age = IntegerField(
        'age', validators=[DataRequired()]
    )
    gender = SelectField(
        'gender',
        validators=[DataRequired()],
        choices=['Female', 'Male'],
        default=''
    )
    email = StringField(
        'email', validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    profile_link = StringField(
        'profile_link', validators=[URL()]
    )
    seeking_student = SelectField(
        'seeking_student',
        validators=[DataRequired()],
        choices=['Yes', 'No'],
        default=''
    )
    seeking_description = StringField(
        'seeking_description', validators=[DataRequired()]
    )


class StudentForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    age = IntegerField(
        'age', validators=[DataRequired()]
    )
    gender = SelectField(
        'gender',
        validators=[DataRequired()],
        choices=['Female', 'Male'],
        default=''
    )
    email = StringField(
        'email', validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    profile_link = StringField(
        'profile_link', validators=[URL()]
    )
    seeking_volunteer = SelectField(
        'seeking_volunteer',
        validators=[DataRequired()],
        choices=['Yes', 'No'],
        default=''
    )
    seeking_description = StringField(
        'seeking_description', validators=[DataRequired()]
    )
    