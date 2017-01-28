from django.db import models
from django.contrib.auth.models import User

class ParkPerson(models.Model):

	phone = models.CharField(max_length=25, blank=True)
	user = models.OneToOneField(User, related_name='+', null=True)

	class Meta:
		db_table = 'park_person'
