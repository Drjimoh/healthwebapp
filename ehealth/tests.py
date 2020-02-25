from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Biodata
from django.urls import reverse
from authentication.models import Profile
from django.contrib.auth.models import User
from .serializers import BiodataSerializer

# tests for views


class BaseViewTest(APITestCase):
	client = APIClient()

	@staticmethod
	def create_biodata(patient="", weight="",
		height="", blood_pressure="", status=""):
		if patient != "" and weight != "" and height !="" and blood_pressure!="" and status!="":
			Biodata.objects.create(patient=patient, weight=weight,
				height=height, blood_pressure=blood_pressure, status=status)

	def setUp(self):
		profile_instance=Profile.objects.create(user=User.objects.create_user("ololade", "W1a2l3i"))
		profile_instance = Profile.objects.all()[0]
		# add test data
		self.create_biodata(profile_instance, 79, 167, "133/88", "good")
		self.create_biodata(profile_instance, 77, 167, "112/88", "good")

class GetAllBiodataTest(BaseViewTest):

	def test_get_all_biodata(self):
		response = self.client.get(
			reverse("ehealth:biodata-all")
		)
		# fetch the data from db
		expected = Biodata.objects.all()
		serialized = BiodataSerializer(expected, many=True)
		self.assertEqual(response.data, serialized.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)