from django.conf.urls.defaults import patterns

urlpatterns = patterns('wiki.views',
    (r'^((?:[A-Z]+[a-z]+){2,})/$', 'page'),
    (r'^edit/((?:[A-Z]+[a-z]+){2,})/$', 'edit'),
    (r'^delete/$', 'delete'),
    (r'^$', 'index'),
)
 