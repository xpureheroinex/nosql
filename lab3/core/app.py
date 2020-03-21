from flask import Flask
from flask_restful import Api
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_DB'] = 'lab3'

db = MongoEngine(app)
api = Api(app)
