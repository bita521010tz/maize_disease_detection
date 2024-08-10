# user_registration/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, firstName, lastName, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, firstName=firstName, lastName=lastName, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstName, lastName, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, firstName, lastName, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(max_length=255, blank=True)
    phonenumber = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    def __str__(self):
        return self.email
