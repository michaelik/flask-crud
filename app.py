from os import environ

from flask import Flask
from db import db
from flask_marshmallow import Marshmallow
from flask_restful import Api
from controllers.user_controller import UserController
from errors.error_handlers import register_error_handlers
import logging

"""
This is the entry point of the application
"""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # This will avoid the warning about overhead

# Initialize extensions
db.init_app(app)
ma = Marshmallow(app)
api = Api(app)

# Import and create tables
with app.app_context():
    try:
        """
        Import the models here to ensure they are registered
        This imports all the model files to register tables
        """
        import models  # Ensure all models are imported
        db.create_all()  # Create the tables
        print("Database tables created successfully.")
    except Exception as e:
        logging.error(f"Error creating tables: {e}")

# Register API routes
api.add_resource(UserController, '/users', '/users/<int:id>')

# Register error handlers
register_error_handlers(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
