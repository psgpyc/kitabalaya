from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


from coreaccounts.views import RegistrationView, HomeView
from coreaccounts.forms import UserLoginForm



urlpatterns = [

    path('home', HomeView.as_view(), name='home'),

]
