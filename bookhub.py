from app import app, db
from app.models import User, Recommendation
'''This file serves as a Python script that defines the Flask application instance.'''

#Remember, The Flask application instnce is called app, and is a member of the app package.
# So here, it is importing the app variable that is a member of the app package.

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Recommendation': Recommendation}