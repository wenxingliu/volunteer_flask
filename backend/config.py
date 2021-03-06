# # Grabs the folder where the script runs.
import os
SECRET_KEY = os.urandom(32)

# Enable debug mode.
DEBUG = True

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgres://wenxingliu@localhost:5432/volunteer'

# Auth0 config
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
ALGORITHMS = ['RS256']
API_AUDIENCE = 'volunteer'