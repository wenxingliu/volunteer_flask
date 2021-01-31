from common import app, db, migrate
from models import Volunteer, Student, Classroom

@app.route('/')
def index():
  return 'home'