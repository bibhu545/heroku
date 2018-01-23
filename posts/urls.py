from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import include,url
import posts.views

from django.views.generic import FormView
# from django.conf.urls import patterns, url

urlpatterns = [
    path(r'create/', posts.views.post_create, name='post_create'),
    path(r'<int:id>/', posts.views.post_detail, name='post_detail'),
    path(r'', posts.views.post_list, name='post_list'),
    path(r'<int:id>/edit/', posts.views.post_update, name='post_update'),
    path(r'<int:id>/delete/', posts.views.post_delete, name='post_delete'),
    
    # path(r'admin/', <appname>.views.<function>),
]
