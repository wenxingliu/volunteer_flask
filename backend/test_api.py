import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import app


class BackendTestCases(unittest.TestCase):
    """This class represents the flask app test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "volunteer_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.app.config["SQLALCHEMY_DATABASE_URI"] = self.database_path
            self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
            self.db.app = self.app
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_homepage_success(self):
        res = self.client().get('/home')
        self.assertEqual(res.status_code, 200)

    def test_get_volunteers_missing_authorization(self):
        res = self.client().get('/volunteers')
        self.assertEqual(res.status_code, 401)


if __name__ == "__main__":
    unittest.main()