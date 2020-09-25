from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

default_user_id = 1


class TimeStampModel(models.Model):
    created_by = models.ForeignKey(User, default=default_user_id, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


