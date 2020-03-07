from django.shortcuts import render
from django import views
from django.utils.safestring import mark_safe

from comingsoon.forms import CallToActionForm
from django.shortcuts import render,get_object_or_404, redirect
from comingsoon.models import CallToActionModel
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
import smtplib


class ComingSoonIndexPage(views.View):
    template_name = 'comingsoon/index.html'
    body = 'Congratulations on joining Kitabalaya. You have been successfully registered. '

    def get(self, request, *args, **kwargs):

        ctx = {
            'form': CallToActionForm()
        }
        return render(request, template_name=self.template_name, context=ctx)

    def post(self, request, *args, **kwargs):
        form = CallToActionForm(request.POST)
        ctx = {
            'form': CallToActionForm(),
            'color': 'red',

        }
        if form.is_valid():
            user_email = form.save()

            if form.cleaned_data['email'] not in CallToActionModel.objects.values_list('email')[0]:
                user_email.ip_address = request.META['REMOTE_ADDR']
                user_email.user_agent = request.META['HTTP_USER_AGENT']

                try:
                    email = EmailMessage(
                        subject='Welcome to Kitabalaya.',
                        body=self.body,
                        from_email='contact@kitabalaya.info',
                        to=[form.cleaned_data['email']],
                        reply_to=['contact@kitabalaya.info'],
                        headers={'Content-Type': 'text/plain'},
                    )
                    email.send()
                    messages.success(request, mark_safe('Thank You!!! You are now successfully registered with us.<br>'
                                                        'Please Check Your Email For Exciting Offers.<br>'))
                    user_email.save()

                    return redirect('cta-home')
                except smtplib.SMTPException as e:
                    CallToActionModel.objects.get(email=form.cleaned_data['email']).delete()
                    messages.success(request, mark_safe('Something Went Wrong!! Please try again after few minutes.<br>'
                                                        'If the issue persists, '
                                                        'Please contact us at contact@kitabalaya.info'))
                    return render(request, template_name=self.template_name, context=ctx)

        else:
            messages.error(request, mark_safe('You email is already present in our database.<br>'
                                              ' If you think this is an error, '
                                              '    please contact us at contact@kitabalaya.info'))
            return render(request, template_name=self.template_name, context=ctx)

        return render(request, template_name=self.template_name, context=ctx)





