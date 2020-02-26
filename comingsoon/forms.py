from django import forms
from comingsoon.models import CallToActionModel


class CallToActionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({

            'class': 'cta',
            'placeholder': 'Enter your Email Address',
            'label': ' ',
            'id': 'user-email',
        })

        self.fields['email'].label = ''

    class Meta:
        model = CallToActionModel
        fields = ['email']
