from flask import Blueprint
from lab3.applications.note import routes
from lab3.core.app import app

bp = Blueprint('notes', __name__)

app.register_blueprint(bp)
