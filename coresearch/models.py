from django.db import models


class SearchRecord(models.Model):
    search_parameter = models.CharField(max_length=256, verbose_name='Search Parameter', blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.search_parameter

    class Meta:
        verbose_name_plural = "Search Records"
        verbose_name = "Search Record"



