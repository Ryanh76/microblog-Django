#urls.py
from django.conf.urls import patterns, url

from microblog import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView, name = 'index'),
    url(r'^u/(.*)/$', views.UserView, name = 'user'),
    url(r'^login/', views.LoginView, name = 'login'),
    url(r'^reg/', views.RegView, name = 'reg'),
    url(r'^logout/', views.LogoutView, name = 'logout'),
)
