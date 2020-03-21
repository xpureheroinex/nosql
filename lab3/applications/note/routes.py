from flask_restful import Resource

from nosql.lab3.core.app import api
from nosql.lab3.models.models import Note

_BAD_REQUEST = {'message': 'invalid data', 'status': 400}
_GOOD_REQUEST = {'message': 'ok', 'status': 200}
_NOT_FOUND_REQUEST = {'message': 'not found', 'status': 404}


class Notes(Resource):

    def get(self, note_id):
        note = Note.objects(id=note_id)
        if note is None:
            return _NOT_FOUND_REQUEST
        else:
            response = {'title': note.title,
                        'text': note.text,
                        'user': note.user.id,
                        'last_update': note.last_update}
            return {'notes': response, 'status': 200}


api.add_resource(Notes, '/api/notes/<int:note_id>')

