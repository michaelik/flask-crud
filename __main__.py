import os
from os import environ
from flask import Flask
from db import db
from flask_marshmallow import Marshmallow
from flask_restful import Api
from controllers.user_controller import UserController
from errors.error_handlers import register_error_handlers
from config import config
import logging

"""
This is the entry point of the application
"""

app = Flask(__name__)

# Determine the environment and load the appropriate configuration
env = environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize extensions
db.init_app(app)
ma = Marshmallow(app)
api = Api(app)

# Import and create tables
with app.app_context():
    try:
        db.create_all()  # Create the tables
        logging.info("Database tables created successfully.")
    except Exception as e:
        logging.error(f"Error creating tables: {e}")

# Register API routes
api.add_resource(UserController, '/users', '/users/<int:id>')

# Register error handlers
register_error_handlers(app)

if __name__ == '__main__':
    APP_PORT = int(os.getenv("APP_PORT", 4000))  # Default port to 4000 if not set
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")  # Default host to 0.0.0.0 if not set
    APP_DEBUG = os.getenv("APP_DEBUG", "True").lower() == 'true'  # Convert to boolean
    app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
