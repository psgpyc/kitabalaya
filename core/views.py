from django.contrib.auth import get_user_model
from django.db.models import Prefetch, Q, Avg
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View, DetailView
from coreaccounts.forms import UserLoginForm, RegistrationForm
from corebookmodels.models import Book, Author, RentalCategory, BookRatingModel
from django.db import connection
from core.utils import get_obj_str, get_book_rating, get_date_formatted, get_my_rating

User = get_user_model()
# BookMainCategory.objects.prefetch_related('main_category').all()


class Home(View):
    template_name = 'core/home.html'

    def get(self, request, *args, **kwargs):
        books_rental_category = RentalCategory.objects.prefetch_related('rentalcategory').all()
        ctx = {
            'title': 'Kitabalaya - Rent books from Nepalese and Foreign Authors in Nepal',
            'login_form': UserLoginForm(),
            'registration_form': RegistrationForm(),
            'books_rental_category': books_rental_category,
        }

        return render(request, template_name=self.template_name, context=ctx)


class BookDetails(View):

    def get(self, request, *args, **kwargs):
        slug_name = self.kwargs['slug']
        if request.is_ajax():
            book = Book.objects.filter(slug=slug_name).prefetch_related('book_genre').select_related('author_name')

            if len(book) == 1:
                book_data = {
                    'title': book[0].title,
                    'author': book[0].author_name.name,
                    'summary': book[0].summary,
                    'image': book[0].book_image.url,
                    'published_date': get_date_formatted(book[0]),
                    'page_count': book[0].number_of_pages,
                    'book_condition': book[0].get_book_condition_display(),
                    'quality_rating': book[0].quality_rating,
                    'slug': book[0].slug,
                    'book_genre': get_obj_str(book[0].book_genre.all()),
                    'book_rating': get_book_rating(book[0]),

                }
                return JsonResponse({'book': book_data}, status=200)

        return render(request, template_name='core/test.html', context={})


# class UpdateBookRating(View):
#     template_name = 'core/test.html'
#
#     def get(self, request, *args, **kwargs):
#         if request.is_ajax:
#             pass
#
#     def post(self, request, *args, **kwargs):
#         slug_name = self.kwargs['slug']
#         r_count = request.POST.get('rating_count')
#         if request.is_ajax:
#             user = str(request.user)
#             b_user = User.objects.get(email=user)
#             _book = Book.objects.get(slug=slug_name)
#             try:
#                 book_rating = BookRatingModel.objects.get(Q(created_by=b_user) & Q(book=_book))
#                 book_rating.rating = r_count
#                 book_rating.save()
#
#             except BookRatingModel.DoesNotExist:
#                 book_rating = BookRatingModel.objects.create(created_by=b_user, rating=r_count, book=_book)
#
#             return JsonResponse({'book_rating': book_rating.rating})


