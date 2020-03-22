from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restful import Api

app = Flask(__name__)
app.config['MONGODB_DB'] = 'lab3'

db = MongoEngine(app)
api = Api(app)

from lab3.applications.note import bp as note_bp
app.register_blueprint(note_bp)
