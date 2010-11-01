from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'metz.front.views.index_dav'),
    (r'^(?P<login>\w+)/$', 'metz.front.views.dav_for_user'),
    (r'^(?P<login>\w+)/.*$', 'metz.front.views.dav_for_user'),
)

