from coresearch.models import SearchRecord
from django.forms import ModelForm


class SearchRecordForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SearchRecordForm, self).__init__(*args, **kwargs)
        self.fields['search_parameter'].widget.attrs.update({

            'class': 'cta',
            'placeholder': 'Search Books and Authors',
            'label': ' ',
            'id': 'search-parameter',
        })

        self.fields['search_parameter'].label = ''

    class Meta:
        model = SearchRecord
        fields = ['search_parameter']

