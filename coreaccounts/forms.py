from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe

from coreaccounts.models import ActivateEmail

User = get_user_model()


class RegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({

            'class': 'cta',
            'placeholder': 'Enter your Email Address',
            'id': 'user-email',
        })

        self.fields['full_name'].widget.attrs.update({

            'class': 'cta',
            'placeholder': 'Enter your Full Name',
            'id': 'user-name',
        })

        self.fields['password1'].widget.attrs.update({

            'class': 'cta',
            'placeholder': 'Enter Your password',
            'id': 'user-password1',

        })
        self.fields['password2'].widget.attrs.update({

            'class': 'cta',
            'placeholder': 'Re-enter Your Password',
            'id': 'user-password2',

        })

        self.fields['email'].label = ''
        self.fields['full_name'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    class Meta:
        model = User
        fields = ['full_name','email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(
        label=(''),
        widget=forms.EmailInput(attrs={
                                    'autofocus': True,
                                    'class': 'cta',
                                    'placeholder': 'Enter your Email',
                                    'id': 'email',



                                }))
    password = forms.CharField(
        label=(''),
        strip=False,
        widget=forms.PasswordInput(attrs={
                                        'autocomplete': 'current-password',
                                        'class': 'cta',
                                        'placeholder': 'Enter your Password',
                                        'id': 'password',




        }),)


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
                                label='',
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'cta',
                                        'placeholder': 'Enter your Email',
                                        'id': 'email',
                                }))


class UserPasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetConfirmForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        label=(""),
        widget=forms.PasswordInput(attrs={
            'class': 'cta',
            'placeholder': 'Enter your Password',
            'id': 'password1',

        }),
    )
    new_password2 = forms.CharField(
        label=(""),
        widget=forms.PasswordInput(attrs={
            'class': 'cta',
            'placeholder': 'Re-Enter your Password',
            'id': 'password2',

        }), )


class ReactivateEmailForm(forms.Form):
    email = forms.EmailField(
        label= '',
        widget=forms.EmailInput(
            attrs={
                'class':'cta',
                'placeholder':'Enter you Email',
                'id': 'reactivate-email'
            }
        ),


        max_length=255)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = ActivateEmail.objects.email_exists(email)
        qs_no_email = ActivateEmail.objects.email_doesnot_exists(email)
        if not qs_no_email.exists():
            register_link = reverse('user-register')
            msg = """
                            This email is not present in our database, Would you like to <a href="">Register?</a>
                        """.format(register_link)
            raise forms.ValidationError(mark_safe(msg))

        if not qs.exists():
            reset_link = reverse('password_reset')
            msg = """
                This email has already been activated, Would you like to <a href="">Reset Your Password?</a>
            """.format(reset_link)
            raise forms.ValidationError(mark_safe(msg))
        return email




