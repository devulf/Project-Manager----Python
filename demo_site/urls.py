from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from projects.models import Project
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
url(r'^admin/', include(admin.site.urls)),
url(r'^projects/$', 'projects.views.index'),
url(r'^$', 'projects.views.index'),
url(r'^projects/(?P<project_id>\d+)/$', 'projects.views.detail', name="detail"),
url(r'^projects/add$', 'projects.views.project_add', name="add"),
url(r'^projects/(?P<project_id>\d+)/ticket/add$', 'projects.views.ticket_add', name="ticket_add"),
url(r'^projects/(?P<project_id>\d+)/edit$', 'projects.views.edit', name="edit"),
url(r'^projects/(?P<project_id>\d+)/ticket/(?P<ticket_id>\d+)/edit$', 'projects.views.ticket_edit', name="ticket_edit"),
url(r'^projects/(?P<project_id>\d+)/delete$', 'projects.views.delete', name="delete"),
url(r'^projects/(?P<project_id>\d+)/ticket/(?P<ticket_id>\d+)/delete$', 'projects.views.ticket_delete', name="ticket_delete"),
url(r'^login/$', 'projects.views.login_user'),
url(r'^logout/$', 'projects.views.logout'),
url(r'^projects/(?P<project_id>\d+)/ticket/(?P<ticket_id>\d+)$', 'projects.views.ticket_detail', name="ticket_detail"),
url(r'^projects/search/$','projects.views.search', name="search"),
url(r'^search/$','projects.views.search', name="search"),

)
