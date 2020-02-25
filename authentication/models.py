from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


# Create your models here.

class OTP(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_otp')
    code = models.CharField(max_length=6, default='000000')
    expiry = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'otp'

    def __str__(self):
        return '{}\'s otp - {} '.format(self.code, self.expiry)


class Profile(models.Model):
    user_choices = (
        ('patient', 'patient'),
        ('medicalpractitioner', 'medicalpractitioner'),
        )
    title_choices = (
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Ms', 'Ms'),
        ('Dr', 'Dr')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    usertype = models.CharField(max_length=250, choices=user_choices, default='patient', editable=False)
    title = models.CharField(max_length=5, choices=title_choices, null=True,
                             blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    number = models.CharField(unique=True, max_length=13, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    avatar = models.ImageField(upload_to='profilepictures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    last_login_time = models.DateTimeField( blank=True, null=True)
    otp = models.ForeignKey(OTP, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=200, default='Good')

    class Meta:
        db_table = 'profile'
        ordering = ["-created_at"]

    def __str__(self):
        return F'{self.user}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.avatar:
            self._loaded_avatar = self.avatar
        if self.id:
            self.patient_id = self.id

    def delete(self, **kwargs):
        try:
            self.avatar.delete()
        except:
            pass
        super(Profile, self).delete(**kwargs)


class MedicalPractitioner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    qualification = models.CharField(max_length=250)
    number = models.CharField(unique=True, max_length=13, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    avatar = models.ImageField(upload_to='profilepictures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    last_login_time = models.DateTimeField( blank=True, null=True)
    account_status = models.CharField(max_length=250, choices=(('active', 'active'), ('pending', 'pending')))
    otp = models.ForeignKey(OTP, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'medicalpractitioner'
        ordering = ["-created_at"]

    def __str__(self):
        return F'{self.user} {self.qualification}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.avatar:
            self._loaded_avatar = self.avatar

    def delete(self, **kwargs):
        try:
            self.avatar.delete()
        except:
            pass
        super(MedicalPractitioner, self).delete(**kwargs)
