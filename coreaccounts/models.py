from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    def _create_user(self, email, full_name, phone_number, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('You must set your email username')
        if not full_name:
            raise ValueError('You must set your Full Name')
        if not phone_number:
            raise ValueError('You must set your Phone Number')
        email = self.normalize_email(email)
        full_name = self.model.normalize_username(full_name)
        user = self.model(email=email, full_name=full_name, phone_number=phone_number,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, full_name, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_confirmed', False)
        return self._create_user(email, full_name, phone_number, password, **extra_fields)

    def create_superuser(self, email, full_name, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_confirmed', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, full_name, phone_number, password, **extra_fields)

    def create_staff(self, email, full_name, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is True:
            raise ValueError('Staff Cannot be the Superuser/Admin')

        return self._create_user(email, full_name, phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    class UserGender(models.TextChoices):
        Male = 'M', 'Male',
        Female = 'F', 'Female',
        NonBinary = 'NB', 'Non Binary',
        UnDisclosed = 'UD', 'Prefer not to say'

    email = models.EmailField(max_length=255,
                              unique=True,
                              verbose_name='User Email'
                              )
    phone_number = models.CharField(
                               max_length=14,
                               unique=True,
                               verbose_name='Phone Number',
                                )
    full_name = models.CharField(max_length=100,
                                 verbose_name='Full Name')
    gender = models.CharField(max_length=2,
                              choices=UserGender.choices,
                              default=UserGender.UnDisclosed,
                              blank=True,
                              null=True,
                              verbose_name='Gender'
                              )
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(
                                        default=False,
                                        verbose_name='Email Confirmed?'
                                        )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number']

    def get_full_name(self):
        return self.full_name

    @property
    def staff(self):
        return self.is_staff

    @property
    def is_admin(self):
        return self.is_superuser

    @property
    def active(self):
        return self.is_active

    def __str__(self):
        return self.email


