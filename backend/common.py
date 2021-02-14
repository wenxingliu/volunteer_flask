from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth

from auth.credential import (
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET
)
import config as config  

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.DEBUG

db = SQLAlchemy(app)
migrate = Migrate(app, db)

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=f'https://{config.AUTH0_DOMAIN}',
    access_token_url=f'https://{config.AUTH0_DOMAIN}/oauth/token',
    authorize_url=f'https://{config.AUTH0_DOMAIN}/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)
