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

from models import *

import datetime
import random
import os

@login_required
def info(request):
	if request.method == "POST":
		person = Person.objects.get(user=request.user)
		#BASIC
		name = request.POST.get('name' ,None)
		nickname = request.POST.get('nickname', None)
		birthdate = request.POST.get('birthdate', None)
		birthmonth, birthday, birthyear = birthdate.split("/")
		birthdate = str(birthyear)+"-"+str(birthmonth)+"-"+ str(birthday)
		person.name = name
		person.nickname = nickname
		person.birthdate = birthdate
		#CONTACTS
		principal_address = request.POST.get('principal_address', None)
		alternate_address1 = request.POST.get('alternate_address1', None)	
		alternate_address2 = request.POST.get('alternate_address2', None)
		alternate_address3 = request.POST.get('alternate_address3', None)
		home_phone = request.POST.get('phone_home', None)
		show_home_phone = True if request.POST.get('show_phone_home', None)=="yes" else False
		mobile_phone = request.POST.get('phone_mobile', None)
		show_mobile_phone = True if request.POST.get('show_phone_mobile', None)=="yes" else False
		work_phone = request.POST.get('phone_work', None)
		show_work_phone = True if request.POST.get('show_phone_work', None)=="yes" else False	
		if person.contacts:
			person.contacts.delete()
		contacts = Contacts.objects.create(principal_address=principal_address, alternate_address1=alternate_address1, alternate_address2=alternate_address2, alternate_address3=alternate_address3, home_phone=home_phone, show_home_phone=show_home_phone, mobile_phone=mobile_phone, show_mobile_phone=show_mobile_phone, work_phone=work_phone, show_work_phone=show_work_phone)
		contacts.save()
		person.contacts = contacts
		#EDUCATION
		further_degrees = request.POST.get('further_degrees', None)
		if person.education:
			person.education.further_degrees = further_degrees
		else:
			e = Education.objects.create(further_degrees=further_degrees)
			e.save()
			person.education=e
		person.education.save()
		#CAREER
		job_title = request.POST.get('current_job', None)
		current_company = request.POST.get('current_company', None)
		career_progression = request.POST.get('career_progression', None)
		job_functions = request.POST.getlist('jobs')
		industry_sectors = request.POST.getlist('industries')		
		positions_held = request.POST.get('positions_held', None)
		if person.career:
			person.career.delete()
		career = Career.objects.create(job_title=job_title, current_company=current_company, career_progression=career_progression, positions_held=positions_held)
		career.save()	
		for job in job_functions:
			career.job_functions.add(Job.objects.get(name=job))
		for sector in industry_sectors:
			career.industry_sectors.add(Industry.objects.get(name=sector))
		career.save()
		person.career = career
		#INTERESTS
		website = request.POST.get('website', None)
		facebook_profile = request.POST.get('facebook_profile', None)
		linkedin_profile = request.POST.get('linkedin_profile', None)
		hobbies = request.POST.getlist('hobbies')
		comments = request.POST.get('comments', None)
		languages = request.POST.getlist('languages')
		poli = request.POST.getlist('poli')
		if person.interests:
			person.interests.delete()
		interests = Interests.objects.create(website=website, facebook_profile=facebook_profile, linkedin_profile=linkedin_profile, comments=comments)
		interests.save()
		for hobby in hobbies:
			hobby_name, hobby_category = hobby.split("_")
			interests.hobbies.add(Hobby.objects.get(name=hobby_name, category=hobby_category))
		for language in languages:
			interests.languages.add(Language.objects.get(name=language))
		for p in poli:
			interests.poli.add(Poli.objects.get(name=p))
		interests.save()
		person.interests = interests
		person.save()
		#Spouse	
		marital_status = True if request.POST.get('marital_status', None)=="yes" else False	
		if person.family:
			if person.family.spouse:
				person.family.spouse.delete()
			if person.children:
				person.children.delete()
			person.family.children.delete()
			person.family.delete()
		if marital_status == True:	
			spouse_name = request.POST.get('spouse_name', None)
			spouse_nickname = request.POST.get('spouse_nickname', None)
			spouse_birthdate = request.POST.get('spouse_birthdate', None)
			if spouse_birthdate is not None:	
				spouse_birthmonth, spouse_birthday, spouse_birthyear = spouse_birthda = spouse_birthdate.split("/")
				spouse_birthdate = str(spouse_birthyear)+"-"+str(spouse_birthmonth)+"-"+ str(spouse_birthday)
			show_spouse_birthdate = True if request.POST.get('show_spouse_birthdate', None)=="yes" else False
			spouse_year_graduation = request.POST.get('spouse_year_graduation', None)
			spouse_branch = Branch.objects.get(code=request.POST.get('spouse_branch', None))
			spouse_degree = Degree.objects.get(name=request.POST.get('spouse_degree', None))
			spouse_further_degrees = request.POST.get('spouse_further_degrees', None)
			spouse_roorkee_alum = True if request.POST.get('spouse_roorkee_alum', None)=="yes" else False
			spouse_job_title = request.POST.get('spouse_current_job', None)
			spouse_current_company = request.POST.get('spouse_current_company', None)
			spouse = Spouse.objects.create(name=spouse_name, nickname=spouse_nickname, birthdate=spouse_birthdate, show_birthdate=show_spouse_birthdate, branch_id=spouse_branch.id, graduation_year=spouse_year_graduation, degree_id=spouse_degree.id, roorkee_alum=spouse_roorkee_alum, further_degrees=spouse_further_degrees, job_title=spouse_job_title, current_company=spouse_current_company)
			spouse.save()
			children_number = request.POST.get('child_count', None)
			family = Family.objects.create(spouse_id=spouse.id, children_number=children_number, marital_status=marital_status)
			family.save()
			#CHILDREN
			children_number = int(children_number)
			child_number = children_number
			if child_number > 0:
				while child_number > 0:
					child_name = request.POST.get('child_name'+str(child_number), None)
					child_nickname = request.POST.get('child_nickname'+str(child_number), None)
					child_birthdate = request.POST.get('child_birthdate'+str(child_number), None)
					if child_birthdate is not None:
						child_birthmonth, child_birthday, child_birthyear = child_birthda = child_birthdate.split("/")
						child_birthdate = str(child_birthyear)+"-"+str(child_birthmonth)+"-"+ str(child_birthday)
					show_child_birthdate = True if request.POST.get('show_child_birthdate'+str(child_number), None)=="yes" else False
					child_seeking_matrimony = True if request.POST.get('seeking_matrimony'+str(child_number), None)=="yes" else False
					show_child_matrimony = True if request.POST.get('show_child_matrimony'+str(child_number), None)=="yes" else False
					child_year_graduation = request.POST.get('child_year_graduation'+str(child_number), None)
					child_branch = Branch.objects.get(code=request.POST.get('child_branch'+str(child_number), None))
					child_degree = Degree.objects.get(name=request.POST.get('child_degree'+str(child_number), None))
					child_further_degrees = request.POST.get('child_further_degrees'+str(child_number), None)
					child_roorkee_alum = True if request.POST.get('child_roorkee_alum'+str(child_number), None)=="yes" else False
					child_job_title = request.POST.get('child_current_job'+str(child_number), None)
					child_current_company = request.POST.get('child_current_company'+str(child_number), None)
					child = Child.objects.create(name=child_name, nickname=child_nickname, birthdate="1994-12-12", graduation_year=child_year_graduation, show_birthdate=show_child_birthdate, seeking_matrimony=child_seeking_matrimony, show_matrimony=show_child_matrimony, branch_id=child_branch.id, degree_id=child_degree.id, roorkee_alum=child_roorkee_alum, further_degrees=child_further_degrees, job_title=child_job_title, current_company=child_current_company)
					child.save()
					child_number -= 1
					family.children.add(child)
			family.save()
			person.family=family
			person.save()	
		#messages.success(request, "Details Submitted Successfully.")
		return HttpResponseRedirect("/person/home/")
	else:
		degrees = Degree.objects.all()
		branches = Branch.objects.all()
		jobs = Job.objects.all()
		industries = Industry.objects.all()
		languages = Language.objects.all()
		poli = Poli.objects.all()
		hobbies = Hobby.objects.all()
		try:
			open('/home/iitrteam/public_html/media/profile/'+str(request.user.username))
			image=True
		except IOError as e:
			image = False
		return render_to_response("person/person_info.html",{'image':image,'degrees':degrees,'branches':branches,'jobs':jobs,'industries':industries,'languages':languages,'poli':poli,'hobbies':hobbies},context_instance=RequestContext(request))

@login_required
def personInfo(request):
	response = {}
	if request.method == "POST" and request.is_ajax():
		person = request.user.person
		try:
			a = request.POST['type']
		except:
			return HttpResponse('No type')
		#BASIC
		if request.POST['type']	== "basic":
			name = request.POST.get('name' ,None)
			nickname = request.POST.get('nickname', None)
			birthdate = request.POST.get('birthdate', None)	
			gender = request.POST.get('gender', 'male')
			try:	
				birthmonth, birthday, birthyear = birthdate.split("/")
				birthdate = str(birthyear)+"-"+str(birthmonth)+"-"+ str(birthday)
			except:
				birthdate = None
			person.name = name
			person.nickname = nickname
			person.gender = gender
			if birthdate is not None:	
				person.birthdate = birthdate
			graduation_year = request.POST.get('year_graduation', None)
			branch = Branch.objects.get(code=request.POST.get('branch', None))	
			degree = Degree.objects.get(name=request.POST.get('degree', None))
			if person.education:
				person.education.branch = branch
				person.education.degree = degree
				person.education.graduation_year = graduation_year
				person.education.save()
			else:
				edu = Education.objects.create(branch=branch, degree=degree, graduation_year=graduation_year)
				edu.save()
				person.education = edu
			person.save()
		#CONTACTS
		if request.POST['type'] == "contacts":
			principal_city = request.POST.get('city1', '')
			principal_state = request.POST.get('state1', '')
			principal_country = request.POST.get('country1', '')
			principal_address = request.POST.get('principal_address', None)
			alternate_address1 = request.POST.get('alternate_address1', None)	
			alternate_address2 = request.POST.get('alternate_address2', None)
			alternate_address3 = request.POST.get('alternate_address3', None)
			home_phone = request.POST.get('phone_home', None)
			show_home_phone = True if request.POST.get('show_phone_home', None)=="yes" else False
			mobile_phone = request.POST.get('phone_mobile', None)
			show_mobile_phone = True if request.POST.get('show_phone_mobile', None)=="yes" else False
			work_phone = request.POST.get('phone_work', None)
			show_work_phone = True if request.POST.get('show_phone_work', None)=="yes" else False	
			if person.contacts:
				contacts_dict = {'principal_address':principal_address, 'alternate_address1':alternate_address1, 'alternate_address2':alternate_address2, 'alternate_address3':alternate_address3, 'home_phone':home_phone, 'show_home_phone':show_home_phone, 'mobile_phone':mobile_phone, 'show_mobile_phone':show_mobile_phone, 'work_phone':work_phone, 'show_work_phone':show_work_phone, 'city':principal_city, 'state':principal_state, 'country':principal_country}
				for (key, value) in contacts_dict.items():
					setattr(person.contacts, key, value)
				person.contacts.save()
			else:
				contacts = Contacts.objects.create(principal_address=principal_address, alternate_address1=alternate_address1, alternate_address2=alternate_address2, alternate_address3=alternate_address3, home_phone=home_phone, show_home_phone=show_home_phone, mobile_phone=mobile_phone, show_mobile_phone=show_mobile_phone, work_phone=work_phone, show_work_phone=show_work_phone, city=principal_city, state=principal_state, country=principal_country)
				contacts.save()
				person.contacts = contacts
			print person.contacts.principal_address	
			person.save()
		#EDUCATION
		elif request.POST['type'] == "education":
			further_degrees = request.POST.get('further_degrees', None)
			if person.education:
				person.education.further_degrees = further_degrees
			else:
				e = Education.objects.create(further_degrees=further_degrees)
				e.save()
				person.education=e
			person.education.save()
			person.save()
		#CAREER
		elif request.POST['type'] == "career":
			job_title = request.POST.get('current_job', None)
			current_company = request.POST.get('current_company', None)
			career_progression = request.POST.get('career_progression', None)
			job_functions = request.POST.getlist('jobs')
			industry_sectors = request.POST.getlist('industries')		
			positions_held = request.POST.get('positions_held', None)
			if person.career:
				career_dict = {'job_title':job_title, 'current_company':current_company, 'career_progression':career_progression, 'positions_held':positions_held}
				for (key, value) in career_dict.items():
					setattr(person.career, key, value)
				person.career.save()			
			else:
				career = Career.objects.create(job_title=job_title, current_company=current_company, career_progression=career_progression, positions_held=positions_held)
				career.save()	
				person.career = career
				person.career.save()
			person.save()
			prev_job_functions =  person.career.job_functions.all()
			if len(prev_job_functions) != 0:
				person.career.job_functions.remove(*prev_job_functions)
			prev_industry_sectors =  person.career.industry_sectors.all()
			if len(prev_industry_sectors) != 0:
				person.career.industry_sectors.remove(*prev_industry_sectors)		
			for job in job_functions:
				person.career.job_functions.add(Job.objects.get(name=job))
			for sector in industry_sectors:
				person.career.industry_sectors.add(Industry.objects.get(name=sector))
			person.career.save()
			person.save()
		#INTERESTS
		elif request.POST['type'] == "interests":	
			website = request.POST.get('website', None)
			facebook_profile = request.POST.get('facebook_profile', None)
			linkedin_profile = request.POST.get('linkedin_profile', None)
			hobbies = request.POST.getlist('hobbies')
			comments = request.POST.get('comments', None)
			languages = request.POST.getlist('languages')
			poli = request.POST.getlist('poli')
			if person.interests:
				career_dict = {'website':website, 'facebook_profile':facebook_profile, 'linkedin_profile':linkedin_profile, 'comments':comments}
				for (key, value) in career_dict.items():
					setattr(person.interests, key, value)
				person.interests.save()
				interests = person.interests
			else:
				interests = Interests.objects.create(website=website, facebook_profile=facebook_profile, linkedin_profile=linkedin_profile, comments=comments)
				interests.save()
				person.interests = interests
			prev_hobbies =  person.interests.hobbies.all()
			if len(prev_hobbies) != 0:
				person.interests.hobbies.remove(*prev_hobbies)		
			for hobby in hobbies:
				hobby_name, hobby_category = hobby.split("_")
				interests.hobbies.add(Hobby.objects.get(name=hobby_name, category=hobby_category))
			
			prev_languages =  person.interests.languages.all()
			if len(prev_languages) != 0:
				person.interests.languages.remove(*prev_languages)				
			for language in languages:
				interests.languages.add(Language.objects.get(name=language))
		
			prev_poli =  person.interests.poli.all()
			if len(prev_poli) != 0:
				person.interests.poli.remove(*prev_poli)		
			for p in poli:
				interests.poli.add(Poli.objects.get(name=p))
			interests.save()
			person.interests = interests
			person.save()
		#Spouse	
		elif request.POST['type']	== "family":
			marital_status = True if request.POST.get('marital_status', None)=="yes" else False	
			children_number = request.POST.get('child_count', 0)
			if person.family:
				person.family.marital_status = marital_status
				person.family.children_number = children_number
				person.family.save()
			else:
				family = Family.objects.create(marital_status=marital_status, children_number=children_number)
				family.save()
				person.family = family
				person.save()
			
			if marital_status == True:	
				spouse_name = request.POST.get('spouse_name', None)
				spouse_nickname = request.POST.get('spouse_nickname', None)
				spouse_birthdate = request.POST.get('spouse_birthdate', None)
				try:
					spouse_birthmonth, spouse_birthday, spouse_birthyear = spouse_birthda = spouse_birthdate.split("/")
					spouse_birthdate = str(spouse_birthyear)+"-"+str(spouse_birthmonth)+"-"+ str(spouse_birthday)
				except:
					spouse_birthdate = None
				show_spouse_birthdate = True if request.POST.get('show_spouse_birthdate', None)=="yes" else False
				spouse_year_graduation = request.POST.get('spouse_year_graduation', None)
				spouse_branch = Branch.objects.get(code=request.POST.get('spouse_branch', None))
				spouse_degree = Degree.objects.get(name=request.POST.get('spouse_degree', None))
				spouse_further_degrees = request.POST.get('spouse_further_degrees', None)
				spouse_roorkee_alum = True if request.POST.get('spouse_roorkee_alum', None)=="yes" else False
				spouse_job_title = request.POST.get('spouse_current_job', None)
				spouse_current_company = request.POST.get('spouse_current_company', None)
				if person.family.spouse:
					spouse_dict = {'name':spouse_name, 'nickname':spouse_nickname, 'graduation_year':spouse_year_graduation, 'show_birthdate':show_spouse_birthdate, 'branch':spouse_branch, 'degree':spouse_degree, 'roorkee_alum':spouse_roorkee_alum, 'further_degrees':spouse_further_degrees, 'job_title':spouse_job_title, 'current_company':spouse_current_company}
					for  (key,value) in spouse_dict.items():
						setattr(person.family.spouse, key, value)
						person.family.spouse.save()
				else:
					spouse = Spouse.objects.create(name=spouse_name, nickname=spouse_nickname, show_birthdate=show_spouse_birthdate, branch_id=spouse_branch.id, graduation_year=spouse_year_graduation, degree_id=spouse_degree.id, roorkee_alum=spouse_roorkee_alum, further_degrees=spouse_further_degrees, job_title=spouse_job_title, current_company=spouse_current_company)
					spouse.save()
					person.family.spouse = spouse
				person.family.save()
				person.save()
				if spouse_birthdate is not None:
					person.family.spouse.birthdate = spouse_birthdate
				person.family.spouse.save()
				family=person.family
				#CHILDREN
				children_number = int(children_number)
				child_number = children_number
				
				prev_children = person.family.children.all()
				if len(prev_children) != 0:
					person.family.children.remove(*prev_children)		
			
				if child_number > 0:
					while child_number > 0:
						child_name = request.POST.get('child_name'+str(child_number))
						child_nickname = request.POST.get('child_nickname'+str(child_number))
						child_birthdate = request.POST.get('child_birthdate'+str(child_number))
						try:	
							child_birthmonth, child_birthday, child_birthyear = child_birthda = child_birthdate.split("/")
							child_birthdate = str(child_birthyear)+"-"+str(child_birthmonth)+"-"+ str(child_birthday)
						except:
							child_birthdate = None
						show_child_birthdate = True if request.POST.get('show_child_birthdate'+str(child_number))=="yes" else False
						child_seeking_matrimony = True if request.POST.get('seeking_matrimony'+str(child_number))=="yes" else False
						show_child_matrimony = True if request.POST.get('show_child_matrimony'+str(child_number))=="yes" else False
						child_year_graduation = request.POST.get('child_year_graduation'+str(child_number))
						child_branch = Branch.objects.get(code=request.POST.get('child_branch'+str(child_number)))
						child_degree = Degree.objects.get(name=request.POST.get('child_degree'+str(child_number)))
						child_further_degrees = request.POST.get('child_further_degrees'+str(child_number))
						child_roorkee_alum = True if request.POST.get('child_roorkee_alum'+str(child_number))=="yes" else False
						child_job_title = request.POST.get('child_current_job'+str(child_number))
						child_current_company = request.POST.get('child_current_company'+str(child_number))
						child = Child.objects.create(name=child_name, nickname=child_nickname, birthdate="1994-12-12", graduation_year=child_year_graduation, show_birthdate=show_child_birthdate, seeking_matrimony=child_seeking_matrimony, show_matrimony=show_child_matrimony, branch_id=child_branch.id, degree_id=child_degree.id, roorkee_alum=child_roorkee_alum, further_degrees=child_further_degrees, job_title=child_job_title, current_company=child_current_company)
						if child_birthdate is not None:
							child.birthdate = child_birthdate			
						child.save()
						child_number -= 1
						family.children.add(child)
				family.save()
				person.family=family
				person.save()
		#messages.success(request, "Details submitted succesfully.")
		response['success'] = "Details Submitted successfully."
		return HttpResponse(simplejson.dumps(response), content_type="application/json")
	else:
		id = request.GET.get('id')
		person = request.user.person		
		degrees = Degree.objects.all()
		branches = Branch.objects.all()
		jobs = Job.objects.all()
		industries = Industry.objects.all()
		languages = Language.objects.all()
		poli = Poli.objects.all()
		hobbies = Hobby.objects.all()
		try:
			open('/home/iitrteam/public_html/media/profile/'+str(request.user.username))
			image=True
		except IOError as e:
			image = False

		return render_to_response("person/personInfo.html",{'image':image,'degrees':degrees,'branches':branches,'jobs':jobs,'industries':industries,'languages':languages,'poli':poli,'hobbies':hobbies,'person':person},context_instance=RequestContext(request))

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

@login_required
def imageUpload(request):
	if request.method == 'POST':
		if request.POST.get('submit')	 == "Upload":
			FILE_EXTENSIONS = ("gif", "jpg", "jpeg", "png", "tif")			
			files = request.FILES.getlist('file')
			for file in files:
				if file._size > 2097152:
					messages.error(request, "Please upload an image of size less than 2MB.")
					continue
				if file.name.endswith(FILE_EXTENSIONS):						
					fileName, fileExtension = os.path.splitext(str(file))
					path = '/home/iitrteam/public_html/media/'+'profile/'+str(request.user.username)
					destination = open(path, 'wb+')
					for chunk in file.chunks():
						destination.write(chunk)
						destination.close()
					messages.success(request, "Image uploaded successfully.")
				else:
					messages.error(request, "Please upload a valid image")
		else:
			linkedin_profile = request.user.person.interests.linkedin_profile
			ret = extract_image("http://in.linkedin.com/in/shantanuag", request.user.username)
			if ret:
				messages.success(request, "Image successfully extracted.")
			else:
				messages.error(request, "Image could not be extracted.")
		return HttpResponseRedirect('/person/viewProfile')
	else:
		return HttpResponseRedirect('/person/home')



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
	if request.method == "POST" and request.session['register_post'] == 1:
		name = request.POST.get('name', None)
		gender = request.POST.get('gender', 'male')
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		password1 = request.POST.get('password1', None)
		password2 = request.POST.get('password2', None)
		email = key.email
		branch = request.POST.get('branch', None)
		degree = request.POST.get('degree', None)
		graduation_year = request.POST.get('year_graduation', None)
		username = username + '.' + degree.replace('.','').lower() + '.' + branch.replace('.','').lower() + '.' + str(graduation_year)
		if password1 != password2:
			messages.error(request, "The entered passwords donot match. Please enter again.")
			return HttpResponseRedirect('/person/register/')
		if password != request.session['password'] :
			messages.error(request, "Wrong Key")
			return HttpResponseRedirect('/person/register/')
		try:
			u = User.objects.get(username=username)
			messages.error(request, 'Username '+username+ ' already exists. Choose another username.')
			return HttpResponseRedirect('/person/register/')
		except:
			try:
				b = Branch.objects.get(code=branch)
				d = Degree.objects.get(name=degree)
			except:
				messages.error(request, "Invalid Branch or Degree")
				return HttpResponseRedirect('/person/register/')
			user=User.objects.create(username=username, email=email, date_joined=datetime.date.today(), is_superuser=False)
			user.set_password(password1)
			user.save()
			person=Person.objects.create(user=user, name=name)
			person.save()
			messages.success(request, 'User '+username+' created successfully!')
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

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='')
def deleteUser(request):
	id = request.GET.get('id')
	person = Person.objects.get(id=id)
	username = person.user.username
	try:	
		person.delete()
		messages.success(request, "User " + username + " deleted successfully.")
	except:
		messages.error(request, "There was an error in deleting the user " + username + ". Please try again.")
	return HttpResponseRedirect('/person/home/')

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='')
def flagUser(request):
	id = request.GET.get('id')
	person = Person.objects.get(id=id)
	username = person.user.username
	try:	
	 	person.user.is_active = False
		person.user.save()
		person.save()
		messages.success(request, "User " + username + " flagged successfully.")
	except:
		messages.error(request, "There was an error in flagging the user " + username + ". Please try again.")
	return HttpResponseRedirect('/person/home/')

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='')
def unFlagUser(request):
	id = request.GET.get('id')
	person = Person.objects.get(id=id)
	username = person.user.username
	try:	
	 	person.user.is_active = True
		person.user.save()
		person.save()
		messages.success(request, "User " + username + " unflagged successfully.")
	except:
		messages.error(request, "There was an error in flagging the user " + username + ". Please try again.")
	return HttpResponseRedirect('/person/home/')


@login_required
def home(request):
	persons_count = Person.objects.all().count()
	try:
		usock = urllib.urlopen("http://www.iitr.ac.in")
		pattern = re.compile(r'<div id="news">.*?<div class="rightbottom"',re.DOTALL)
		newsfeed=pattern.search(usock.read()).group(0)
		usock.close()
		newsfeed=newsfeed[:-15]		
	except:
		newsfeed = "News feed unavailable"
	try:
		open('/home/iitrteam/public_html/media/profile/'+str(request.user.username))
		image=True
	except IOError as e:
		image = False

	return render_to_response("person/home.html",{'image':image,'persons_count':persons_count,'person':request.user, 'newsfeed':newsfeed},context_instance=RequestContext(request))


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
		try:
			open('/home/iitrteam/public_html/media/profile/'+str(request.user.username))
			image=True
		except IOError as e:
			image = False

		return render_to_response("person/changePassword.html",{'image':image,},context_instance=RequestContext(request))

