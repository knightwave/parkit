from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
	user = models.OneToOneField(User, related_name='person')
	name = models.CharField(max_length=100)
	contactNumber = models.CharField(max_length=20)


class LocationMetadata(models.Model):
	name = models.CharField(max_length=254)
	latitude = models.CharField(max_length=20)
	longitude = models.CharField(max_length=20)
	address = models.CharField(max_length=254)


# Assumption made: Same cost for parking at all times of a day for a given location
class ParkingSpot(models.Model):
	cost = models.DecimalField(max_digits=4, decimal_places=2, default=0.0) # per hour
	maxTime = models.PositiveIntegerField(null=True, default=300) # in minutes
	minTime = models.PositiveIntegerField(null=True, default=30) # in minutes
	location = models.ForeignKey(LocationMetadata)


class Booking(models.Model):
	person = models.ForeignKey(User, related_name='bookings')
	parkingSpot = models.ForeignKey(ParkingSpot, related_name='bookings')
	startTime = models.DateTimeField()
	endTime = models.DateTimeField()
	isActive = models.BooleanField(default=True)
