# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext 
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder


from models import *
from constants import EXPECTED_DURATIONS

import json
import datetime
import random
import os
import requests
from dateutil.relativedelta import relativedelta

@login_required
def info(request):
	if request.method == "POST":
		return HttpResponseRedirect("/person/home/")
	else:
		return render_to_response("person/person_info.html",{'image':image,'degrees':degrees,'branches':branches,'jobs':jobs,'industries':industries,'languages':languages,'poli':poli,'hobbies':hobbies},context_instance=RequestContext(request))


@login_required
def viewProfile(request):
	id = request.GET.get('id', None)
	if id is not None:
		try:		
			person = Person.objects.get(id=id)
		except:
			person = request.user.person
	else:
		person=request.user.person

	return render_to_response("person/viewProfile.html",{'image':False,'person':person, 'person_image':False},context_instance=RequestContext(request))



def loginRequest(request):
	errors = []
	success = []
	if request.user.is_authenticated():	
		return HttpResponseRedirect('/person/home/')
	if request.method=="POST":
		username=request.POST.get('username', None)
		password=request.POST.get('password', None)
		user=authenticate(username=username,password=password)
		
		if user is not None and user.is_active:
			login(request,user)
			if not request.POST.get('remember_me', None):
				request.session.set_expiry(0)		
			return HttpResponseRedirect("/person/home/")		
		messages.error(request, "Please enter valid details. Login Failed.")
	return render_to_response("person/login.html",{'errors':errors,'success':success},context_instance=RequestContext(request))

def logoutRequest(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/person/login')
	logout(request)
	return HttpResponseRedirect('/person/login')


def register(request):
	errors = []
	success = []
	if request.method == "POST":
		name = request.POST.get('name', None)
		email = request.POST.get('email', None)
		password1 = request.POST.get('password1', None)
		password2 = request.POST.get('password2', None)
		phone = request.POST.get('phone', None)
		inputs = {
			'name': name,
			'email': email,
			'phone': phone,
		}
		if password1 != password2:
			messages.error(request, "The entered passwords donot match. Please enter again.")
			return HttpResponseRedirect('/person/register/')
		try:
			u = User.objects.get(username=email, email=email)
			messages.error(request, 'Email '+email+ ' already exists. Choose another username.')
			return render_to_response('register.html',{'inputs': inputs},context_instance=RequestContext(request))
		except:
			user=User.objects.create(username=email, email=email)
			user.set_password(password1)
			user.save()
			person=Person.objects.create(user=user, name=name, contactNumber=phone)
			person.save()
			messages.success(request, 'Email ' + email + ' created successfully!')
			return HttpResponseRedirect('/person/login/')
	else:
		return render_to_response('register.html',{},context_instance=RequestContext(request))

def loginRequest(request):
	errors = []
	success = []
	if request.user.is_authenticated():	
		return HttpResponseRedirect('/person/home/')
	if request.method=="POST":
		username=request.POST.get('username', None)
		password=request.POST.get('password', None)
		user=authenticate(username=username,password=password)
		if user is not None and user.is_active:
			login(request,user)
			if not request.POST.get('remember_me', None):
				request.session.set_expiry(0)		
			return HttpResponseRedirect("/person/home/")		
		messages.error(request, "Please enter valid details. Login Failed.")
	return render_to_response("person/login.html",{'errors':errors,'success':success},context_instance=RequestContext(request))


def getData(lat, lng, duration):
	start = datetime.datetime.utcnow()
	end = start + relativedelta(minutes=int(duration))
	url = "http://api.parkwhiz.com/search/?lat={0}&lng={1}&key=62d882d8cfe5680004fa849286b6ce20&start={2}&end={3}".format(str(lat), str(lng), start.strftime("%s"), end.strftime("%s"))
	response = requests.get(url)
	if response.status_code != 200:
		return {}

	listings = json.loads(response.text).get('parking_listings', {})
	return listings

def isOccupied(location):
	latitude = location['lat']
	longitude = location['lng']
	try:
		parkingSpot = ParkingSpot.objects.get(latitude=latitude, longitude=longitude)
	except ParkingSpot.DoesNotExist:
		parkingSpot = ParkingSpot.objects.create(address=location['address'], latitude=latitude, longitude=longitude)

	startTime = datetime.datetime.fromtimestamp(int(location['start']))
	endTime = datetime.datetime.fromtimestamp(int(location['end']))
	currentActiveBookings = Booking.objects.filter(
		isActive=True,
		startTime__range=(startTime, endTime),
		endTime__range=(startTime, endTime),
		parkingSpot=parkingSpot,
	)
	location['remainingSpots'] = parkingSpot.totalSpots - currentBookings.count()
	if location['remainingSpots']:  # All spots are occupied
		return False, parkingSpot

	return True, parkingSpot

def checkAndCreateBooking(location):
	isSpotOccupied, parkingLocation = isOccupied(location)
	if isSpotOccupied:
		return

	return Booking.objects.create(
		parkingSpot=parkingLocation,
		startTime=location['start'],
		endTime=location['end'],
		cost=location['cost'],
	)

@login_required
def home(request):
	showMap = False
	inputData = {}
	parkingLocations = {}
	jsonLocation = None
	if request.method == "POST":
		showMap = True
		parkingDuration = request.POST.get('parkingDuration', None)
		jsonLocation = request.POST.get('jsonLocation', None)
		location = json.loads(jsonLocation)
		latitude = location['lat']
		longitude = location['lng']
		inputData['latitude'] = latitude
		inputData['longitude'] = longitude
		inputData['parkingDuration'] = parkingDuration
		inputData['jsonLocation'] = jsonLocation
		inputData['autoCompletePlace'] = request.POST.get('autoCompletePlace', None)
		parkingLocations = getData(latitude, longitude, parkingDuration)
		parkingLocations = [parkingLocation for parkingLocation in parkingLocations if not isOccupied(parkingLocation)[0]]

	return render_to_response("person/home.html",
		{
			'EXPECTED_DURATIONS':EXPECTED_DURATIONS,
			'person':request.user,
			'showMap': showMap,
			'parkingLocations': parkingLocations,
			'inputData': inputData,
		},
		context_instance=RequestContext(request))

@login_required
def book(request):
	if request.method == "POST":
		jsonLocation = request.POST.get('parkingLocation', None)
		location = json.loads(jsonLocation)
		booking = checkAndCreateBooking(location)
		if not booking:
			messages.error("There is an active booking already for this duration")
		else:
			messages.success("Parking successfully booked at ".format(location['address']))

	return HttpResponseRedirect("/person/profile/")

@login_required
def profile(request):
	return render_to_response("person/profile.html",{'image':image},context_instance=RequestContext(request))

@login_required
def changePassword(request):
	if request.method == "POST":
		old_password = request.POST.get('old_password', None)
		new_password1 = request.POST.get('new_password1', None)
		new_password2 = request.POST.get('new_password2', None)
		if new_password1 != new_password2:
			messages.error(request,"The new passwords donot match")
			return HttpResponseRedirect('')
		user = Person.objects.get(user=request.user).user
		if user.check_password(old_password):
			user.set_password(new_password1)
			user.save()
			messages.success(request, "Password Changed Successfully.")
		else:
			messages.error(request, "Please enter your password correctly")
		return HttpResponseRedirect('')
	else:
		return render_to_response("person/changePassword.html",{'image':False},context_instance=RequestContext(request))

