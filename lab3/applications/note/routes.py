from flask_restful import Resource, reqparse

from lab3.core.app import api
from lab3.models.models import Note, User

_BAD_REQUEST = {'message': 'invalid data', 'status': 400}
_GOOD_REQUEST = {'message': 'ok', 'status': 200}
_NOT_FOUND_REQUEST = {'message': 'not found', 'status': 404}


class Notes(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('Authorization', location='headers')
        self.parser.add_argument('text')

    def get(self, note_id):
        args = self.parser.parse_args()
        if args['Authorization'] is None:
            return {'message': 'Unauthorized', 'status': 401}
        token = args['Authorization'].split(' ')[1]
        user_id = User.verify_auth_token(token)['user_id']
        user = User.objects(id=user_id).first()
        if user is None:
            return _BAD_REQUEST
        note = Note.objects(id=note_id).first()
        if note is None:
            return _NOT_FOUND_REQUEST
        else:
            response = {'title': note.title,
                        'text': note.text,
                        'user': note.user.id,
                        'last_update': note.last_update}
            return {'notes': response, 'status': 200}

    def put(self, note_id):
        args = self.parser.parse_args()
        note_text = args['text']
        if args['Authorization'] is None:
            return {'message': 'Unauthorized', 'status': 401}
        token = args['Authorization'].split(' ')[1]
        user_id = User.verify_auth_token(token)['user_id']
        user = User.objects(id=user_id).first()
        if user is None:
            return _BAD_REQUEST
        note = Note.objects(id=note_id).first()
        if note is None:
            return _NOT_FOUND_REQUEST
        elif note.user.id == user.id:
            if note_text:
                note.text = note_text
                note.set_last_update()
                note.save()
                return {'message': 'Note was successfully updated!', 'status': 201}
            return _BAD_REQUEST
        else:
            return {'message': 'Forbidden', 'status': 403}

    def delete(self, note_id):
        args = self.parser.parse_args()
        if args['Authorization'] is None:
            return {'message': 'Unauthorized', 'status': 401}
        token = args['Authorization'].split(' ')[1]
        user_id = User.verify_auth_token(token)['user_id']
        user = User.objects(id=user_id).first()
        if user is None:
            return _BAD_REQUEST
        note = Note.objects(id=note_id).first()
        if note is None:
            return _NOT_FOUND_REQUEST
        elif note.user.id == user.id:
            note.delete()
            return _GOOD_REQUEST
        else:
            return {'message': 'Forbidden', 'status': 403}


api.add_resource(Notes, '/api/notes/<int:note_id>')


class UserNotes(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('Authorization', location='headers')
        self.parser.add_argument('title')
        self.parser.add_argument('text')

    def post(self, user_id):
        args = self.parser.parse_args()
        note_title = args['title']
        note_text = args['text']

        if args['Authorization'] is None:
            return {'message': 'Unauthorized', 'status': 401}
        token = args['Authorization'].split(' ')[1]
        user_id_from_token = User.verify_auth_token(token)['user_id']
        if user_id_from_token != user_id:
            return _BAD_REQUEST

        user = User.objects(id=user_id).first()
        if user is None:
            return _NOT_FOUND_REQUEST
        elif note_title is not None and note_text is not None:
            note = Note(
                title=note_title,
                text=note_text,
                user=user
            )
            note.set_last_update()
            note.save()
            return {'message': 'Note was successfully created!', 'status': 201}
        else:
            return _BAD_REQUEST

    def get(self, user_id):
        args = self.parser.parse_args()
        if args['Authorization'] is None:
            return {'message': 'Unauthorized', 'status': 401}
        token = args['Authorization'].split(' ')[1]
        user_id_from_token = User.verify_auth_token(token)['user_id']
        if user_id_from_token != user_id:
            return _BAD_REQUEST

        user = User.objects(id=user_id).first()
        if user is None:
            return _NOT_FOUND_REQUEST
        else:
            notes = Notes.objects(user=user)
            note_list = []
            for note in notes:
                info = {
                    'id': note.id,
                    'title': note.title,
                    'text': note.text,
                    'user': note.user.id,
                    'last_update': note.last_update
                }
                note_list.append(info)
            return {'notes': note_list, 'status': 200}


api.add_resource(UserNotes, '/api/users/<int:user_id>/notes')


class Search(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('Authorization', location='headers')
        self.parser.add_argument('search')

    def get(self):
        args = self.parser.parse_args()
        search = args['search']
        if args['Authorization'] is None:
            return {'message': 'Unauthorized', 'status': 401}
        token = args['Authorization'].split(' ')[1]
        if User.verify_auth_token(token) is None:
            return {'message': 'Unauthorized', 'status': 401}
        user_id = User.verify_auth_token(token)['user_id']
        user = User.objects(id=user_id)
        if user is None:
            return _BAD_REQUEST
        elif search is not None:
            note_list = []
            research = search.strip()
            # search by title or text???
            notes = Note.objects(user=user, title=research).all()

            for note in notes:
                info = {'title': note.title,
                        'text': note.text,
                        'user': note.user.id,
                        'last_update': note.last_update}
                note_list.append(info)
            return {'notes': note_list, 'status': 200}
        return _BAD_REQUEST


api.add_resource(Search, '/api/notes/search')
