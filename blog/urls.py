from django.conf.urls import url
from django.urls import path
from .views import Home

urlpatterns = [

    path('', Home.as_view(), name='blog-homepage'),
]


