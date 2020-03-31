from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^role/list', views.role_list, name="role_list"),
    url(r'^role/add', views.role_change, name="role_add"),
    url(r'^role/edit/(?P<pk>\d+)', views.role_change, name="role_edit"),
    url(r'^menu/list', views.menu_list, name="menu_list"),
    url(r'^menu/add', views.menu_change, name="menu_add"),
    url(r'^menu/edit/(?P<pk>\d+)', views.menu_change, name="menu_edit"),
    url(r'^permission/add/', views.permission_change, name="permission_add"),
    url(r'^permission/edit/(?P<pk>\d+)', views.permission_change, name="permission_edit"),

    url(r'^multi/permissions/$', views.multi_permissions, name='multi_permissions'),

    url(r'^delete/(?P<table>\w+)/(?P<pk>\d+)', views.delete, name="delete"),
]
