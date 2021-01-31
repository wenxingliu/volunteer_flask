from common import db, app, migrate


# Volunteer - Classroom: One to many
volunteer_classroom = db.Table('volunteer_classroom',
    db.Column('volunteer_id', db.Integer, db.ForeignKey('volunteer.id'), primary_key=True),
    db.Column('classroom_id', db.Integer, db.ForeignKey('classroom.id'), primary_key=True)
)

# Student - Classroom: One to many
student_classroom = db.Table('student_classroom',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('classroom_id', db.Integer, db.ForeignKey('classroom.id'), primary_key=True)
)


class Volunteer(db.Model):
    __tablename__ = 'volunteer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    email = db.Column(db.String(50), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    profile_link = db.Column(db.String(120), nullable=False)
    seeking_student = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(), nullable=False)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise Exception(f"Failed to register Volunteer {self.name}")
        finally:
            db.session.close()

    def short(self):
        volunteer_info = {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "seeking_student": str(self.seeking_student)
        }
        return volunteer_info

    def __repr__(self):
        return f'<Volunteer {self.id}: {self.name} (Age {self.age})>'


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    email = db.Column(db.String(50), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    profile_link = db.Column(db.String(120), nullable=False)
    seeking_volunteer = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(), nullable=False)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise Exception(f"Failed to register Student {self.name}")
        finally:
            db.session.close()

    def short(self):
        student_info = {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "seeking_volunteer": str(self.seeking_volunteer)
        }
        return student_info

    def __repr__(self):
        return f'<Student {self.id}: {self.name} (Age {self.age})>'


class Classroom(db.Model):
    __tablename__ = 'classroom'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    time = db.Column(db.Time, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    volunteer_id = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Volunteer {self.volunteer_id}: Student {self.student_id}>'
