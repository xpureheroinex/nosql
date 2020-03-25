from flask import Blueprint
from lab3.applications.note import routes

bp = Blueprint('notes', __name__)
