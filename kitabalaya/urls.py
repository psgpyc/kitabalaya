from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from core.views import Categories, SubCategoryView
from coreaccounts.forms import UserPasswordResetForm,UserPasswordResetConfirmForm,UserLoginForm
from coreaccounts.views import RegistrationView, UserLogoutView, AccountEmailActivate, UserLoginView
from cart.views import InitCart

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # USER ACCOUNTS

    path('register/', RegistrationView.as_view(), name='user-register'),

    # path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True,
    #      template_name='coreaccounts/login.html',
    #      authentication_form=UserLoginForm), name='user-login'),

    path('login/', UserLoginView.as_view(), name='user-login'),

    path('logout/',
         login_required(UserLogoutView.as_view(template_name='coreaccounts/login.html', )),
         {'next_page': settings.LOGOUT_REDIRECT_URL}, name='user-logout'),

    path('reset/',
         auth_views.PasswordResetView.as_view(
             template_name='coreaccounts/password_reset_form.html',
             form_class=UserPasswordResetForm,
         ),

         name='password_reset'),
    path('reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='coreaccounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='coreaccounts/password_reset_confirm.html',
             form_class=UserPasswordResetConfirmForm,

         ),
         name='password_reset_confirm'),
    path('reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='coreaccounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    re_path(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$',
            AccountEmailActivate.as_view(),
            name='email-activate'),

    # END USER ACCOUNTS

    path('', include('comingsoon.urls'), name='base-coreaccounts'),
    path('home/', include('core.urls'), name='base-home'),
    path('categories/<slug:slug>/', Categories.as_view(), name='categories-main'),
    path('categories/<slug:mainCategory>/<slug:subCategory>/', SubCategoryView.as_view(), name='sub-category'),

    path('cart/', include('cart.urls'), name='cart'),

    # API URLS

    path('api/', include('coreaccounts.api.api-urls'), name='base-api-url')

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # import debug_toolbar
    #
    # urlpatterns = [
    #                   path('__debug__/', include(debug_toolbar.urls)),
    #               ] + urlpatterns
