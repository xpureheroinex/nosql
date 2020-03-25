from flask import Blueprint

bp = Blueprint('users', __name__)

from lab3.applications.user import routes
