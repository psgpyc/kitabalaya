
from django.contrib import admin
from django.urls import path
from comingsoon.views import ComingSoonIndexPage

urlpatterns = [

    path('', ComingSoonIndexPage.as_view(), name='cta-home'),

]
