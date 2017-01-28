from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.models import User
from person.models import ParkPerson

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def registrationView(request):
	error_message=''

	print "pramod"
	print request.POST
	if request.POST:
		firstName = request.POST.get('park_first_name', None)
		lastName = request.POST.get('park_last_name', None)
		email = request.POST.get('park_email', None)
		phoneNumber = request.POST.get('park_phone', None)
		password = request.POST.get('park_password', None)
		if not firstName or not lastName or not email or not phoneNumber or not password:
			error_message='Please fill all details.'

		elif User.objects.filter(email='email').exists():
			error_message='A user is already registered with this email'

		else:
			us = User.objects.create(
					first_name=firstName,
					last_name=lastName,
					email=email
				)

			ParkPerson.objects.create(
				phone=phoneNumber,
				user=us
			)
			return render(
			request,
				'registrationSuccess.html',
			)


	return render(
		request,
		'registration.html',
		{
			'error_message':error_message
		},
	)
