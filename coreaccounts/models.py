from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.core.mail import send_mail
from django.template.loader import get_template
from coreaccounts.utils import random_string_generator
from django.urls import reverse

import random

DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVE_DAYS', 1)


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


class ActivateEmailQuerySet(models.query.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        end_range = now
        return self.filter(
            activated=False,
            forced_expired=False
        ).filter(
            created_on__gt=start_range,
            created_on__lte=end_range
        )


class ActivateEmailManager(models.Manager):
    def get_queryset(self):
        return ActivateEmailQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()


class ActivateEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    email = models.EmailField(max_length=255, unique=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)
    activated = models.BooleanField(default=False)
    path_key = models.CharField(max_length=120)
    forced_expired = models.BooleanField(default=False)

    objects = ActivateEmailManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = ActivateEmail.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_active = True
            user.save()
            self.activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.path_key = None
        self.save()

        if self.path_key is not None:
            return True
        else:
            return False

    def send_activation_email(self):
        if not self.activated and not self.forced_expired:
            if self.path_key:
                base_url = getattr(settings, 'BASE_URL', 'https://www.kitabalaya.com/')
                path = reverse("email-activate", kwargs={'key': self.path_key})
                url_path = "{base}{path}".format(base=base_url, path=path)
                context = {
                    'path': url_path,
                    'email': self.email
                }

                txt_ = get_template('coreaccounts/verify.txt').render(context)
                html_ = get_template('coreaccounts/verify.html').render(context)
                subject = 'Account registration on www.kitabalaya.com'
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'contact@kitabalaya.info')

                sent_email = send_mail(
                    subject=subject,
                    message=txt_,
                    from_email=from_email,
                    recipient_list=(self.email,),
                    html_message=html_,
                    fail_silently=False,
                )
        return False


def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.path_key:
            size = random.randint(35,45)
            key = random_string_generator(size=size)
            qs = ActivateEmail.objects.filter(path_key__iexact=key)
            if qs.exists():
                key = random_string_generator(size=size)

            instance.path_key = key


pre_save.connect(pre_save_email_activation, sender=ActivateEmail)


def post_save_user_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        obj = ActivateEmail.objects.create(user=instance, email=instance.email)
        obj.send_activation_email()


post_save.connect(post_save_user_create_receiver, sender=User)
