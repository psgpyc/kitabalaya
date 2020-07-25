from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages


from corebookmodels.models import Book
from marathon.models import SubscribedBook


class HomeView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            selected_team = SubscribedBook.objects.get(user=user)
        except SubscribedBook.DoesNotExist:
            selected_team = None
        if selected_team is not None:
            return redirect('team-profile')
        qs = Book.objects.filter(has_contest=True)
        print(qs)

        ctx = {
            'books': qs,
        }
        return render(request, template_name='marathon/home.html', context=ctx)

    def post(self, request, *args, **kwargs):
        book, user = request.POST['book_obj'], request.user
        book_obj = Book.objects.get(title=book)
        if book_obj is not None and user is not None:
            SubscribedBook.objects.create(user=user, book=book_obj)

            msg = "Congratulations on joining team {}".format(book_obj.team_name)
            messages.success(request, msg)
            return redirect('team-profile')

        return render(request, template_name='marathon/home.html')


class TeamView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            team_obj = SubscribedBook.objects.get(user=user)
        except SubscribedBook.DoesNotExist:
            team_obj = None

        if team_obj is not None:
            ctx = {
                'book_name': team_obj
            }
        else:
            msg = "You have been Kicked out of your Team. Please Join another team below."
            messages.success(request, msg)
            return redirect('home')

        return render(request, template_name='marathon/team-display.html', context=ctx)