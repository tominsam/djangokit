from django.conf.urls.defaults import *
from django.conf import settings
import re

from django.contrib import admin
admin.autodiscover()

def app_to_pattern(name):
    return (r'^'+re.escape(name)+"/", include('%s.urls'%name))

built = [ (r'^admin/(.*)', admin.site.root), ] + map( app_to_pattern, settings.APPS )

urlpatterns = patterns('', *built)
