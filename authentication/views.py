from django.shortcuts import render, redirect, HttpResponse
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile, OTP, MedicalPractitioner
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from .utils import unique_generator, format_phone_number
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate

# Create your views here.

def index(request):
	return render(request, 'authentication/signup.html', {})

def join(request):
	return render(request, 'authentication/signup.html', {})


def staff_join(request):
	return render(request, 'authentication/staff_signup.html', {})

def validate_username(request):
	username = request.GET.get('username', None)
	data = {
		'is_taken': User.objects.filter(username__iexact=username).exists()
	}
	return JsonResponse(data)


def validate_email(request):
	email = request.GET.get('email', None)
	data = {
		'is_taken': User.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)

def login(request):
	return render(request, 'authentication/login.html', {})

def reset(request):
	return render(request, 'authentication/reset.html', {})

def set_new_pass(request):
	return render(request, 'authentication/set_new_pass.html', {})
	
def logout(request):
	try:
		del request.session['username']
	except:
		pass
	return redirect(reverse('authentication:login'))


@api_view(['GET', 'POST'])
def auth(request):
	if request.method == 'POST':
		target = request.POST.get('target')
		data = {
			'status': 400
		}
		context = {}
		if target == "login":
			data = {'response': "login"}
			username = request.POST.get('username').strip()
			password = request.POST.get('password').strip()
			user = authenticate(request, username=username, password=password)
			try:
				if user:
					if Profile.objects.get(user=user).usertype == 'patient':
						request.session['username'] = username
						try:
							user_instance = Profile.objects.get(user=User.objects.get(username=username))
							user_instance.last_login_time = timezone.now()
							user_instance.save()
						except Exception as e:
							print(e)
						return redirect(reverse('ehealth:patient_dash'))
					else:
						status = MedicalPractitioner.objects.get(user=user)
						if status.account_status != 'pending':
							request.session['username'] = username
							try:
								user_instance = MedicalPractitioner.objects.get(user=User.objects.get(username=username))
								user_instance.last_login_time = timezone.now()
								user_instance.save()
							except Exception as e:
								print(e)
							return redirect(reverse('ehealth:health_dash'))
						else:
							return HttpResponse("Account currently undergoing verification, contact admin if problem persists after 24hrs")
				else:
					print('error, invalid username or password')
					return render(request, 'authentication/login.html', {'error':'error'})
			except:
				try:
					status = MedicalPractitioner.objects.get(user=user)
					if status.account_status != 'pending':
						request.session['username'] = username
						try:
							user_instance = MedicalPractitioner.objects.get(user=User.objects.get(username=username))
							user_instance.last_login_time = timezone.now()
							user_instance.save()
						except Exception as e:
							print(e)
						return redirect(reverse('ehealth:health_dash'))
					else:
						return HttpResponse("Account currently undergoing verification, contact admin if problem persists after 24hrs")
				except:
					pass
				return HttpResponse("Unexpected error, try again ")
		elif target == "reset":
			q = request.POST.get
			username = q('username', '')
			otp = q('otp')
			password1 = q('password1', '')
			password2 = q('password2', '')
			user = Profile.objects.get(user=User.objects.get(username=username))
			if user.otp.code == otp:
				if password1 == password2:
					user = User.objects.get(username=username)
					user.set_password(password1)
					user.save()
					data = {
							'status':'password changed successfully, login now'
						}
					return JsonResponse(data)
				else:
					data = {
							'status':'passwords do not match, try again'
						}
					return JsonResponse(data)
			else:
				data = {
						'status':'invalid otp'
					}
				return JsonResponse(data)
		elif target == "signup":
			q = request.POST.get
			firstname = q('fname', '')
			lastname = q('lname', '')
			username = q('username')
			email = q('email')
			number = q('number')
			password1 = q('password1')
			password2 = q('password2')
			if password1 == password2:
				try:
					# print(request.POST.get('fname'))
					# print(q('fname'))
					user = User.objects.create_user(username, email, password1)
					user = User.objects.get(username=username)
					profile = Profile.objects.create(user=user, first_name=firstname, 
						last_name=lastname, number=number)
					profile.save()
					data = {
						'status':'successful',
					}
					# send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, fail_silently=True)
					return JsonResponse(data)
				except Exception as e:
					print(e)
					e = str(e)
					data = {
						'status':'e'
					}
					return JsonResponse(data)
			else:
				data = {
					'status':'password mismatch'
				}
				return JsonResponse(data)
		elif target == "staff-signup":
			q = request.POST.get
			firstname = q('fname', '')
			lastname = q('lname', '')
			username = q('username')
			email = q('email')
			qualification = q('qualification')
			number = q('number')
			password1 = q('password1')
			password2 = q('password2')
			if password1 == password2:
				try:
					# print(request.POST.get('fname'))
					# print(q('fname'))
					user = User.objects.create_user(username, email, password1)
					user = User.objects.get(username=username)
					staff = MedicalPractitioner.objects.create(user=user, first_name=firstname, 
						last_name=lastname, number=number, qualification=qualification)
					staff.save()
					data = {
						'status':'successful',
					}
					# send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, fail_silently=True)
					return JsonResponse(data)
				except Exception as e:
					print(e)
					e = str(e)
					data = {
						'status':'e'
					}
					return JsonResponse(data)
			else:
				data = {
					'status':'password mismatch'
				}
				return JsonResponse(data)
		elif target == "retrieve":
			data = {'response': 'retrieve'}
			try:
				username = request.POST.get('username').strip()
				print(username)
				try:
					if str(username).isnumeric():
						number = format_phone_number(username)
						if number:
							user = Profile.objects.get(number=number)
						else:
							user = Profile.objects.get(user=User.objects.get(email=username))
					else:
						user = Profile.objects.get(user=User.objects.get(email=username))
						print(user)
				except:
					user = None

				if user:
					otp = unique_generator(OTP, 'code', length=6, allowed_chars='0123456789')
					otp_user = OTP.objects.create(code=otp, 
													expiry=timezone.now() + timedelta(minutes=15),
													status=True)
					otp_user.save()
					user.otp = otp_user
					user.save()
					current_site = get_current_site(request)
					domain = current_site.domain
					scheme = 'https' if request.is_secure() else 'http'
					url = "{0}://{1}/reset/".format(scheme, domain)
					print(url)
					subject = 'Reset Password'
					message = f'''Dear {user.user.username},

You just requested for a password reset
follow this link  {url} and use {otp} as your passkey.
Kindly ignore this mail if this wasn't you.  

Regards, 
Meditech Support
								''' 
					from_email = settings.EMAIL_HOST_USER
					recipient_list = [user.user.email]
					send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, fail_silently=True)
					send_alert.after_response(user, 'retrieve', {'url': url, 'otp': otp})

					data['details'] = "A reset link has been sent to your phone and/or email"
					data['redirect'] = reverse('authentication:login')
					data['status'] = 200
				else:
					data['details'] = "User not found."
					data['status'] = 400
			except Exception as e:
				print(str(e))
				data['details'] = "Wow this is embarrassing, we couldn't initialize the reset process."
				data['status'] = 404

		return JsonResponse(data, safe=False, status=data['status'])
	else:
		user = request.user
		context = {}
		if user and user.is_authenticated:
			return redirect('authentication:index')
		return render(request, 'authentication/login.html', context)
