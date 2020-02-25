from . import views
from django.urls import path


app_name = 'authentication'

urlpatterns = [
	path('', views.index, name='index'),
    path('signup', views.join, name='join'),
    path('staff/signup', views.staff_join, name='staff_join'),
    path('ajax/validate_username', views.validate_username, name='validate_username'),
 	path('ajax/validate_email', views.validate_email, name='validate_email'),
 	path('login', views.login, name='login'),
 	path('auth', views.auth, name='auth'),
 	path('logout', views.logout, name='logout'),
 	path('reset/', views.reset, name='reset'),
 	path('set_new_pass/', views.set_new_pass, name='set_new_pass'),
]