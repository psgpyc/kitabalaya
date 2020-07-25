from django.urls import path
from marathon.views import HomeView, TeamView

urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('team-profile', TeamView.as_view(), name='team-profile')

]
