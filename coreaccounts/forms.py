from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



User = get_user_model()


class RegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({

            'class': 'cta',
            'placeholder': 'Enter your Email Address',
            'id': 'user-email',
        })
        self.fields['phone_number'].widget.attrs.update({

            'class': 'cta',
            'placeholder': 'Enter your Phone Number',
            'id': 'user-phone',
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
        self.fields['phone_number'].label = ''
        self.fields['full_name'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    class Meta:
        model = User
        fields = ['full_name','email', 'phone_number', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(
                                label='',
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'cta',
                                        'placeholder': 'Enter your Email',
                                        'id': 'email',
                                }))
    password = forms.CharField(
        label=(''),
        widget=forms.PasswordInput(
            attrs={
                'class': 'cta',
                'placeholder': 'Enter your Password',
                'id': 'password',
            }))

