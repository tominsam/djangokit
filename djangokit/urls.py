from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),

    # default
    (r'^', include('%s.urls'%settings.APPNAME)),

)
