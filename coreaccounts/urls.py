from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


from coreaccounts.views import RegistrationView, HomeView
from coreaccounts.forms import UserLoginForm

urlpatterns = [
    path('register', RegistrationView.as_view(), name='user-register'),
    path('login/', auth_views.LoginView.as_view(template_name='coreaccounts/login.html',authentication_form=UserLoginForm
), name='user-login'),
    path('logout/', login_required(auth_views.LogoutView.as_view(template_name='coreaccounts/logout.html')), name='users-logout'),

    path('home', HomeView.as_view(), name='home')
]
