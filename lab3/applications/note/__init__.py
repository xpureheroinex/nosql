from flask import Blueprint
from nosql.lab3.applications.note import routes
from nosql.lab3.core.app import app

bp = Blueprint('notes', __name__)

app.register_blueprint(bp)
