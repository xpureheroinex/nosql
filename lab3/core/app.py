from flask import Flask
from flask_restful import Api
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_DB'] = 'lab3'

db = MongoEngine(app)
api = Api(app)

from lab3.applications.user import bp as user_bp

app.register_blueprint(user_bp)
