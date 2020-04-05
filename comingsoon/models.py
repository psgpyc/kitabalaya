from django.db import models


class CallToActionModel(models.Model):
    email = models.EmailField(unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{}, {}".format(self.email, self.created_date.date())

    class Meta:
        verbose_name = 'Call to action'
        verbose_name_plural = 'call to action'









