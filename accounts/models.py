from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
import datetime


class User(AbstractUser):
    email = models.EmailField(max_length=255, verbose_name='email address', unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        """
        return True

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        return True

    @property
    def is_staff(self):
        """
        Is the user a member of staff?
        """
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(default='1.jpg')
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
