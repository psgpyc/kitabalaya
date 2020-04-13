from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.shortcuts import render,redirect
from coreaccounts.models import ActivateEmail
from coreaccounts.forms import RegistrationForm, ReactivateEmailForm
from django.contrib.auth.views import LogoutView, LoginView
from coreaccounts.forms import UserLoginForm
from django.urls import reverse
from django.utils.safestring import mark_safe


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

        print(name, request.POST.get('password2'))
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('full_name')
            print(username)
            messages.success(request,
                             'Hey {} ! Your account has been Registered. '
                             'Please check your email to activate your account.'.format(username))
            return redirect('user-register')

        return render(request, template_name=self.template_name,
                      context={'form': form, 'title':'Registration| Kitabalaya'
                     })


class HomeView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        return render(request, template_name='coreaccounts/home.html')


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
        qs = ActivateEmail.objects.filter(path_key__iexact=key)
        qs_confirm = qs.confirmable()
        print(qs_confirm)
        if qs_confirm.count() == 1:
            obj = qs.first()
            obj.activate()
            messages.success(request, 'Your Email has been confirmed. '
                                      'You can now login to Kitabalaya using your email and password.')
            return redirect('user-login')
        else:
            qs_activated = qs.filter(activated=True)
            if qs_activated.exists():
                reset_link = reverse('password_reset')
                msg = """
                    You have already confirmed your Email address. In case you forget,
                    Do you want to <a href={}>reset your password?</a>
                """.format(reset_link)
                messages.success(request, mark_safe(msg))
                return redirect('user-login')
        ctx = {'form':self.get_form()}
        return render(request, template_name='coreaccounts/registration-error.html', context=ctx)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        obj = ActivateEmail.objects.email_exists(email).first()
        if obj.regenerate():
            obj.send_activation_email()
        return super(AccountEmailActivate, self).form_valid(form)

    def form_invalid(self, form):

        ctx = {'form':self.get_form()}
        return render(self.request, template_name='coreaccounts/registration-error.html', context=ctx)

