from django.conf.urls import patterns, include, url
from django.conf import settings

from . import views

urlpatterns = patterns('',
	url(r'^register/$', views.register),
	url(r'^login/$', views.loginRequest),
	url(r'^home/$', views.home),
	url(r'^viewProfile/$', views.viewProfile),
 #    (r'^profile/$', 'alumni.person.views.personInfo'),
 #    (r'^changePassword/$', 'alumni.person.views.changePassword'),
	# (r'^confirm/(?P<confirmation_key>\w+)/$', 'alumni.person.views.confirmUser'),
	# (r'^confirmEmail/(?P<confirmation_key>\w+)/$', 'alumni.person.views.confirmEmail'),	
	# (r'^register/$', 'alumni.person.views.register'),
	# (r'^deleteUser/$', 'alumni.person.views.deleteUser'),
	# (r'^home/$', 'alumni.person.views.home'),
 #    (r'^logout/$', 'alumni.person.views.logoutRequest'),
 #    (r'^viewProfile/$', 'alumni.person.views.viewProfile'),
	# (r'^deleteUser/(?P<username>[\w|\W]+)/$', 'alumni.person.views.deleteUser'),
)

