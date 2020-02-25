from django.db import models
from authentication.models import Profile, MedicalPractitioner
# Create your models here.


class Case(models.Model):
	name = models.CharField(max_length=120, blank=True, null=True)
	lethality = models.CharField(max_length=150, 
		choices=(
			('serious', 'serious'),
			('moderate', 'moderate'),
			('terminal', 'terminal'), ))

	def __str__(self):
		return self.name 

class Biodata(models.Model):
	patient = models.ForeignKey(Profile, on_delete=models.CASCADE)
	weight = models.IntegerField()
	weight_unit = models.CharField(choices=(('kg', 'kilograme'), ('Ibs', 'Pounds')), max_length=250, blank=True, null=True)
	height = models.IntegerField()
	blood_pressure = models.CharField(max_length=250)
	age = models.CharField(max_length=250,  blank=True)
	bmi = models.CharField(max_length=250, blank=True)
	blood_glucose_level = models.CharField(max_length=250, blank=True)
	last_clinic_visit = models.DateTimeField(blank=True, null=True)
	date_of_birth = models.DateTimeField(blank=True, default='2001-03-30')
	disabilities = models.CharField(max_length=250, blank=True)
	allergies = models.CharField(max_length=250, blank=True)
	status = models.CharField(max_length=200, default='Good')

	class Meta:
		db_table = 'biodata'

	def __str__(self):
		return f"{self.patient} {self.last_clinic_visit}"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.weight and self.height:
			self.bmi = self.weight/((self.height/100)**2)

class Appointment(models.Model):
	patient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='patient')
	doctor_seen = models.ForeignKey(MedicalPractitioner, on_delete=models.SET_NULL, null=True, related_name='doctor')
	clinical_manifestations = models.TextField()
	diagnosis = models.ForeignKey(Case, on_delete=models.SET_NULL, null=True)
	prescription = models.CharField(max_length=250)
	next_appointment = models.DateTimeField()

	class Meta:
		db_table = 'appointment'

	def __str__(self):
		return f"{self.patient} {self.diagnosis}"
