from multiselectfield import MultiSelectField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, dob, password=None):
        if not email:
            raise ValueError("Email is mandatory.")
        user = self.model(
            email = self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            dob=dob,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, dob, password=None):
        user = self.create_user(email, first_name, last_name, dob, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=40, verbose_name="First Name")
    last_name = models.CharField(max_length=40, verbose_name="Last Name")
    dob = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_practitioner = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "dob", "password"]

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=255)
    healthcare_number = models.CharField(max_length=15)


class Practitioner(models.Model):
    SPECIALIZATION = (
        (1, "backache"),
        (2, "Visceral Osteopathy"),
        (3, "Pregnancy Osteopathy"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=255)
    diploma = models.CharField(max_length=15)
    specialization = MultiSelectField(choices=SPECIALIZATION)
