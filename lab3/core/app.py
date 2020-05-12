from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_DB'] = 'lab3'
app.config["SECRET_KEY"] = 'verysecretkeywowsecurrrrrity'

db = MongoEngine(app)
api = Api(app)
CORS(app)

from lab3.applications.note import bp as note_bp
app.register_blueprint(note_bp)

from lab3.applications.user import bp as user_bp

app.register_blueprint(user_bp)
