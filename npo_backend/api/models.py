from django.db import models
from mongoengine import *
# Create your models here.


class User(Document):
    name = StringField(required=True)
    email = EmailField(required=True)
    password = StringField(required=True)
