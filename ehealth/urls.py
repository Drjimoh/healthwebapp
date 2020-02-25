from django.urls import path
from . import views
from django.conf.urls import url 

app_name = 'ehealth'

urlpatterns = [
	# path('biodata/', views.biodata_fill, name='biodata_fill'),
	# path('patients/', views.patient_stats, name='patient_stats'),
	path('staff/dashboard', views.health_dash, name='health_dash'),
	path('patient/dashboard', views.patient_dash, name='patient_dash'),
	path('patient/editbio', views.edit_bio, name='edit_bio'),
	path('patient/mybio', views.my_bio, name='my_bio'),
	path('patient/updatebio', views.update_bio, name='updatebio'),
	path('staff/all-patients', views.all_patients, name='all_patients'),
	url(r'^patient/(?P<id>[-\w]+)/$', views.patient_bio, name="patient_bio"),
	path('', views.homepage, name='homepage'),
	path('all-doctors', views.all_doctors, name='all_doctors'),
	path('biodata/', views.ListBiodataView.as_view(), name="biodata-all"),
]
