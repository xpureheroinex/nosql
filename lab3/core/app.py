from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restful import Api

app = Flask(__name__)
app.config['MONGODB_DB'] = 'lab3'

db = MongoEngine(app)
api = Api(app)
