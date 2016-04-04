# coding=utf-8
from django.conf.urls import patterns, include, url

from django.contrib import admin
import views

admin.autodiscover()

urlpatterns = patterns('',
    # 官网
    url(r'^$', views.com_index),
    url(r'^com_courier', views.com_courier),
    url(r'^com_business', views.com_business),
    url(r'^com_privacy', views.com_privacy),
    url(r'^com_backend', views.com_backend),
    url(r'^com_profile', views.com_profile),
    url(r'^update_avatar', views.update_avatar),
    url(r'^answer', views.get_answer),
)