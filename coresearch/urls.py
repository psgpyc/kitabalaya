from django.contrib import admin
from django.urls import path, include
from coresearch.views import SearchHome

urlpatterns = [
    path('', SearchHome.as_view(), name='search-home')


]