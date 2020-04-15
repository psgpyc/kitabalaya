from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class HomeView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, template_name='marathon/home.html')