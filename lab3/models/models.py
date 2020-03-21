import datetime

from flask_mongoengine import Document
from mongoengine import IntField, StringField, DateTimeField, ReferenceField, CASCADE


class User(Document):
    id = IntField(primary_key=True)
    username = StringField(required=True)
    password = StringField(required=True)


class Note(Document):
    id = IntField(primary_key=True)
    title = StringField(required=True)
    text = StringField(required=True)
    user = ReferenceField('User', reverse_delete_rule=CASCADE)
    last_update = DateTimeField(required=True, default=datetime.datetime.utcnow())
