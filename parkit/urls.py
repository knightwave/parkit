from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'parkit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^person/', include('person.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': '/Users/knightwave/parkit/media/', 'show_indexes': True}),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
