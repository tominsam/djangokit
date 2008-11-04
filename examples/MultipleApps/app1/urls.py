from django.conf.urls.defaults import *
from app1.models import *

info_dict = {
    'queryset': Todo.objects.all().order_by('date'),
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list',
        dict(info_dict, allow_empty = True )
    ),
)
