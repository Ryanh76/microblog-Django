from django.db import models
from mongoengine import *
# Create your models here.
connect('microblog')

class posts(Document):
    user = StringField(required = True)
    post = StringField(max_length=140)
    time = DateTimeField()


