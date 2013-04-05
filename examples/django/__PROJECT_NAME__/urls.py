"""
{{ PROJECT_NAME }}.urls
-----------------------
"""

from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template


admin.autodiscover()
urlpatterns = patterns('')

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^404/$', direct_to_template, {'template': '404.html'},
            name='404'),
        url(r'^500/$', direct_to_template, {'template': '500.html'},
            name='500'),
    )

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)
