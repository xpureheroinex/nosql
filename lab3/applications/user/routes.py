from flask_restful import Resource, reqparse
from lab3.core.app import api
from lab3.models.models import User

_BAD_REQUEST = {'message': 'invalid data', 'status': 400}
_GOOD_REQUEST = {'message': 'ok', 'status': 200}
_NOT_FOUND_REQUEST = {'message': 'not found', 'status': 404}


class Register(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', required=True)
        self.parser.add_argument('password', required=True)

    def post(self):
        args = self.parser.parse_args()

        username = args['username']
        password = args['password']

        user = User.objects(username=username).first()

        if user is not None:
            return {'status': 404,
                    'message': f'User with username = {username} already exists!'}
        elif username is not None and password is not None:
            user = User(
                id=User.generate_id(),
                username=username
            )
            user.set_password(password)

            user.save()

            return {'message': 'User was successfully created!', 'status': 201}
        else:
            return _BAD_REQUEST


api.add_resource(Register, '/api/users/register')


class Login(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', required=True)
        self.parser.add_argument('password', required=True)

    def post(self):
        args = self.parser.parse_args()

        username = args['username']
        password = args['password']

        user = User.objects(username=username).first()

        if user is None:
            return {'status': 404,
                    'message': f'User with username = {username} does not exist!'}
        else:
            if user.check_password(password):
                token = user.generate_auth_token(expiration=10000)
                tkn = str(token)
                tkn = tkn[2:len(tkn) - 1]
                return {'message': 'ok', 'status': 200, 'Bearer': tkn}, {'Bearer': token}
            return _BAD_REQUEST


api.add_resource(Login, '/api/users/login')


class Users(Resource):

    def get(self):
        users = User.objects
        response = []
        for user in users:
            info = {
                'id': user.id,
                'username': user.username
            }
            response.append(info)

        return {'users': response, 'status': 200}


api.add_resource(Users, '/api/users')


class UserProfile(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('old_password', required=True)
        self.parser.add_argument('new_password', required=True)
        self.parser.add_argument('Authorization', location='headers')

    def put(self):
        args = self.parser.parse_args()

        old_password = args['old_password']
        new_password = args['new_password']

        if args['Authorization'] is None:
            return {'message': 'Unauthorized', 'status': 401}
        token = args['Authorization'].split(' ')[1]
        if User.verify_auth_token(token) is None:
            return {'message': 'Unauthorized', 'status': 401}
        user_username = User.verify_auth_token(token)['username']
        user = User.objects(username=user_username).first()
        if user is None:
            return _BAD_REQUEST
        else:
            if user.check_password(old_password):
                if new_password:
                    user.set_password(new_password)

                    user.save()

                    return {'message': 'User was successfully updated!', 'status': 201}
                return _BAD_REQUEST
            else:
                return _BAD_REQUEST


api.add_resource(UserProfile, '/api/user')
