from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class firstOTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)



class User(AbstractUser):
    typeChoice = (("1", 'Admin'), ("2", "Manager"), ("3", "General"))
    roleChoice = (("1", 'Head'), ("2", "Developer"), ("3", "Tester"))
    userType = models.CharField(max_length=100, choices=typeChoice)
    userRole = models.CharField(max_length=100, choices=roleChoice)
    is_verified = models.BooleanField(default=False)
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'auth_user'

# class userType(models.Model):
#     userTypeId = models.AutoField(primary_key=True)
#     userTypeName = models.CharField(max_length=100, null=False)
#
# class userRole(models.Model):
#     userRoleId = models.AutoField(primary_key=True)
#     userRoleName = models.CharField(max_length=100, null=False)