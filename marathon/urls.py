from django.urls import path
from marathon.views import HomeView

urlpatterns = [

    path('', HomeView.as_view(), name='home'),

]
