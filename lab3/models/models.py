import datetime

from flask_mongoengine import Document

from lab3.core.app import app

from mongoengine import IntField, StringField, DateTimeField, ReferenceField, CASCADE
from werkzeug.security import generate_password_hash, check_password_hash

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired


class User(Document):
    id = IntField(primary_key=True)
    username = StringField(required=True)
    password = StringField(required=True)

    def __init__(self, username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expiration=None):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id, 'username': self.username})

    @staticmethod
    def generate_id():
        latest_id = User.objects.order_by('-id').first().id
        return latest_id + 1

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user_id = data['id']
        username = data['username']
        return {'user_id': user_id, 'username': username}


class Note(Document):
    id = IntField(primary_key=True)
    title = StringField(required=True)
    text = StringField(required=True)
    user = ReferenceField('User', reverse_delete_rule=CASCADE)
    last_update = DateTimeField(required=True, default=datetime.datetime.utcnow())

    def __init__(self, title, text, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.text = text
        self.user = user

    def set_last_update(self):
        self.last_update = datetime.datetime.utcnow()
