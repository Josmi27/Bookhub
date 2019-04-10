from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
'''This file serves as the Flask application instance, which creates the application 
object as an instance of class Flask imported from the flask package.'''



#__name__ = a Python predefined variable that is set to the name of the module in which it is used
# __name__ is passed to Flask so that the location of the module can be used as a starting point when it
# needs to load "associated resources such as template files". So it serves as a starting place.
app = Flask(__name__)
app.config.from_object(Config)
#SQLAlchemy is an ORM, which allows applications to manage a database using high-level entities 
#such as classes, objects, and methods into tables
db = SQLAlchemy(app)
#migrate represents the migration engine. Migrate is a wrapper for Alembic, a database migration framework for SQLAlchemy 
migrate = Migrate(app, db)

login = LoginManager(app)

#used for when user that is not logged in tries to access a protected page
login.login_view = 'login'
from app import routes, models