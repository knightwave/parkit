from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
	user = models.OneToOneField(User, related_name='person')
	name = models.CharField(max_length=100)
	contactNumber = models.CharField(max_length=20)

	@property
	def activeBookings(self):
		return self.bookings.filter(isActive=True).order_by('-id')

	@property
	def inactiveBookings(self):
		return self.bookings.filter(isActive=False).order_by('-id')

class ParkingSpot(models.Model):
	name = models.CharField(max_length=254)
	latitude = models.CharField(max_length=20)
	longitude = models.CharField(max_length=20)
	address = models.CharField(max_length=254)
	maxTime = models.PositiveIntegerField(null=True, default=300) # in minutes
	minTime = models.PositiveIntegerField(null=True, default=30) # in minutes
	totalSpots = models.IntegerField(default=10)

class Booking(models.Model):
	person = models.ForeignKey(Person, related_name='bookings')
	parkingSpot = models.ForeignKey(ParkingSpot, related_name='bookings')
	startTime = models.DateTimeField()
	endTime = models.DateTimeField()
	isActive = models.BooleanField(default=True)
	cost = models.DecimalField(max_digits=4, decimal_places=2, default=0.0) # Cost of booking is fetched dynamically
