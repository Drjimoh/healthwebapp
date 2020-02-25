from django.shortcuts import render, reverse, redirect
from authentication.models import Profile, MedicalPractitioner
from .models import Case, Biodata, Appointment 
from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import generics 
from .serializers import BiodataSerializer



# for test case
class ListBiodataView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Biodata.objects.all()
    serializer_class = BiodataSerializer



def health_dash(request):
	cases = set(Appointment.objects.all().values_list("diagnosis").annotate(freq=Count("diagnosis")))
	case_list = []
	patient_list = Biodata.objects.all()
	doctors_list = MedicalPractitioner.objects.filter(account_status='active')
	for case in cases:
		case_dict = {}
		case_dict['name'] = Case.objects.get(id=case[0]).name
		patients_affected = Appointment.objects.filter(diagnosis=Case.objects.get(id=case[0]))
		case_dict['freq'] = case[1]
		case_dict['patients_affected'] = patients_affected
		case_list.append(case_dict)
	print(case_list)
	if request.session.has_key('username'):
		try:
			profile = Profile.objects.get(user=User.objects.get(username=request.session['username']))
			if profile:
				return redirect(reverse('authentication:login'))
		except:
			doctors_list = MedicalPractitioner.objects.filter(account_status='active')
			return render(request, 'ehealth/Preclinic-Hospital/index.html', 
			{'patient_list':patient_list, 'doctors':len(doctors_list), 
			'case_list':case_list, 'patients':len(patient_list)})
	else:
		return redirect(reverse('authentication:login'))	

def update_bio(request):
	username = request.session['username']
	if request.method == 'POST':
		q = request.POST.get
		weight = q('weight', '')
		height = q('height', '')
		disabilities = q('disabilities', '')
		allergies = q('allergies', '')
		dob = q('dob', '')
		gender =q('gender', '')
		blood_pressure = q('bloodp', '')
		age = q('age', '')	
		try:
			old_bio = Biodata.objects.get(
				patient=Profile.objects.get(user=User.objects.get(username=username)))
			old_bio.delete()
		except Exception as e:
			print(e)
		biodata_instance = Biodata.objects.create(
			patient=Profile.objects.get(user=User.objects.get(username=username)),
			weight=int(weight),
			height=int(height),
			age= age,
			date_of_birth=dob,
			blood_pressure = blood_pressure,
			disabilities=disabilities,
			allergies=allergies,
			)
		biodata_instance.save()
		return render(request, 'ehealth/Preclinic-Hospital/index-2.html', {})

def patient_dash(request):
	if request.session.has_key('username'):
		return render(request, 'ehealth/Preclinic-Hospital/index-2.html', {})
	else:
		return redirect(reverse('authentication:login'))
def all_patients(request):
	patient_list = Biodata.objects.all()
	return render(request, 'ehealth/Preclinic-Hospital/all-patients.html', {'patient_list':patient_list})

def all_doctors(request):
	if request.session.has_key('username'):
		try:
			profile = Profile.objects.get(user=User.objects.get(username=request.session['username']))
			if profile:
				doctors_list = MedicalPractitioner.objects.filter(account_status='active')
				return render(request, 'ehealth/Preclinic-Hospital/all-doctors.html', 
					{'doctors_list':doctors_list, 'patient':'true'})
		except:
			doctors_list = MedicalPractitioner.objects.filter(account_status='active')
			return render(request, 'ehealth/Preclinic-Hospital/homepage.html', 
					{'doctors_list':doctors_list, 'doctor':'true'})
	else:
		doctors_list = MedicalPractitioner.objects.filter(account_status='active')
		print('&'*100)
		return render(request, 'ehealth/Preclinic-Hospital/all-doctors.html', {'doctors_list':doctors_list})


def edit_bio(request):
	return render(request, 'ehealth/Preclinic-Hospital/edit_bio.html', {})

def my_bio(request):
	username= request.session['username']
	try:
		bio = Biodata.objects.get(patient=Profile.objects.get(
			user=User.objects.get(username=username)))
		return render(request, 'ehealth/Preclinic-Hospital/my_biodata.html', {'bio':bio})
	except:
		return render(request, 'ehealth/Preclinic-Hospital/my_biodata.html', {})



def patient_bio(request, id):
	if request.session.has_key('username'):
		username = request.session['username']
		bio = Biodata.objects.get(patient=Profile.objects.get(id=int(id)))
		return render(request, 'ehealth/Preclinic-Hospital/patient-bio.html', {'bio':bio
							  })
	return redirect(reverse('authentication:login'))

def homepage(request):
	cases = set(Appointment.objects.all().values_list("diagnosis").annotate(freq=Count("diagnosis")))
	case_list = []
	for case in cases:
		case_dict = {}
		case_dict['name'] = Case.objects.get(id=case[0]).name
		case_dict['freq'] = case[1]
		case_list.append(case_dict)
	if request.session.has_key('username'):
		try:
			profile = Profile.objects.get(user=User.objects.get(username=request.session['username']))
			if profile:
				doctors_list = MedicalPractitioner.objects.filter(account_status='active')
				return render(request, 'ehealth/Preclinic-Hospital/homepage.html', 
					{'doctors_list':doctors_list, 
					'patient':'true',
					 'case_list':case_list})
		except:
			doctors_list = MedicalPractitioner.objects.filter(account_status='active')
			return render(request, 'ehealth/Preclinic-Hospital/homepage.html', 
					{'doctors_list':doctors_list, 'doctor':'true', 'case_list':case_list})
	else:
		doctors_list = MedicalPractitioner.objects.filter(account_status='active')
		return render(request, 'ehealth/Preclinic-Hospital/homepage.html', 
					{'doctors_list':doctors_list, 'case_list':case_list})

