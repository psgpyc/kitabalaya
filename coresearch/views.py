from django.shortcuts import render

from django.views.generic import TemplateView
from coresearch.forms import SearchRecordForm



class SearchHome(TemplateView):
    template_name = 'coresearch/basesearch.html'

    def get(self, request, *args, **kwargs):

        ctx = {
            'form': SearchRecordForm()
        }
        return render(request, template_name=self.template_name, context=ctx)