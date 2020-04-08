from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.shortcuts import render,redirect
from coreaccounts.forms import RegistrationForm


class RegistrationView(View):
    template_name = 'coreaccounts/reg.html'
    ctx = {
        'form': RegistrationForm(),
        'title': 'Registration| Kitabalaya'
    }

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context=self.ctx)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        name = request.POST.get('password1')

        print(name,request.POST.get('password2'))
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('full_name')
            print(username)
            messages.success(request,
                             'Hey {} ! Your account has been created. Please Login to continue.'.format(username))
            return redirect('registration')

        return render(request, template_name=self.template_name, context={'form': form,         'title': 'Registration| Kitabalaya'
})


class HomeView(View, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        return render(request, template_name='coreaccounts/home.html')

