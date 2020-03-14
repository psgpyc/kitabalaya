from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class User(AbstractBaseUser, models.Model):
    pass


