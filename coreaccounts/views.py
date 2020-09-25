from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import forms
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormMixin, FormView
from django.contrib import messages
from django.shortcuts import render, redirect
from coreaccounts.models import ActivateEmail
from coreaccounts.forms import RegistrationForm, ReactivateEmailForm
from django.contrib.auth.views import LogoutView
from coreaccounts.forms import UserLoginForm
from django.urls import reverse
from django.utils.safestring import mark_safe


class UserLoginView(View):
    template_name = 'coreaccounts/login.html'

    ctx = {
        'form': UserLoginForm(),
        'title': 'Login| Kitabalaya',
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        return render(request, template_name=self.template_name, context=self.ctx)

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            login(request, form.get_user())

            if request.is_ajax():
                print('ajax request')
                json_data = {
                    'logged_in': 'true',
                    'messages': 'Successfully logged in!'
                }

                return JsonResponse(json_data)
            return redirect('home')

        if request.is_ajax():
            print('ajax request')
            json_data = {
                'logged_in': 'false',
                'messages': 'Please enter a correct email and password. Note that both fields may be case-sensitive.'
            }

            return JsonResponse(json_data)

        return render(request, template_name=self.template_name, context={'form':form})


class RegistrationView(View):
    template_name = 'coreaccounts/reg.html'
    ctx = {
        'form': RegistrationForm(),
        'title': 'Registration| Kitabalaya'
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        return render(request, template_name=self.template_name, context=self.ctx)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        name = request.POST.get('password1')
        registered = False

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('full_name')
            registered = True

            messages.success(request,
                             'Hey {} ! Your account has been Registered. '
                             'Please check your email to activate your account.'.format(username))
            if request.is_ajax():
                json_data = {
                    'registered': registered,
                    'messages': 'Hey {} ! Your account has been Registered. '
                                'Please check your email to activate your account.'.format(username)
                }

                return JsonResponse(json_data)

            return redirect('user-register')

        if request.is_ajax():
            json_data = {
                'form_error_message': form.errors,
                'registered': False,
                'messages': 'Hey! Your account has not  been Registered. '

            }
            return JsonResponse(json_data)
        return render(request, template_name=self.template_name,
                      context={'form': form, 'title': 'Registration| Kitabalaya'})


class UserLogoutView(LogoutView):
    def __init__(self, *args, **kwargs):
        super(UserLogoutView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserLoginForm()

        return context


class AccountEmailActivate(FormMixin, View):
    form_class = ReactivateEmailForm
    success_url = '/reset/done/'

    def get(self, request, key, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        qs = ActivateEmail.objects.filter(path_key__iexact=key)
        qs_confirm = qs.confirmable()
        if qs_confirm.count() == 1:
            obj = qs.first()
            obj.activate()
            msg = """
                Your Email has been confirmed. <br>
                You can now log in to Kitabalaya using your Email and Password.
            
            """
            messages.success(request, mark_safe(msg), extra_tags='email_confirmed')

            return redirect('home')
        else:
            qs_activated = qs.filter(activated=True)
            if qs_activated.exists():
                reset_link = reverse('password_reset')
                msg = """
                    You have already confirmed your Email address. <br> In case you forget,<br>
                    Do you want to <a href={}>reset your password?</a>
                """.format(reset_link)
                messages.success(request, mark_safe(msg), extra_tags='email_confirmed')
                return redirect('home')
        ctx = {'form': self.get_form()}
        return render(request, template_name='coreaccounts/registration-error.html', context=ctx)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = """
        Activation link has been sent to you, Please check your Email.
        """
        messages.success(self.request, msg)
        email = form.cleaned_data.get('email')
        obj = ActivateEmail.objects.email_exists(email).first()
        if obj.regenerate():
            obj.send_activation_email()
        return super(AccountEmailActivate, self).form_valid(form)

    def form_invalid(self, form):

        ctx = {'form': self.get_form()}
        return render(self.request, template_name='coreaccounts/registration-error.html', context=ctx)
