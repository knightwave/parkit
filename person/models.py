from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
	user = models.OneToOneField(User, related_name='person')
	name = models.CharField(max_length=100)
	contactNumber = models.CharField(max_length=20)
