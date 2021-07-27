from django.contrib.auth import get_user_model
from django.db.models import Prefetch, Q, Avg
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View, DetailView
from coreaccounts.forms import UserLoginForm, RegistrationForm
from corebookmodels.models import Book, Author, RentalCategory, Banner, BookBelongsTo, \
    BookMainCategory, BookCategory, Genre, Language, BookBelongsTo
from django.db import connection
from core.utils import get_obj_str, get_date_formatted, get_curr_url, get_cart_count, get_breadcrumbs
import json
from django.core.paginator import Paginator
from django.core import serializers
from django.db.models import Q
from functools import reduce
import operator



User = get_user_model()
# BookMainCategory.objects.prefetch_related('main_category').all()


class Home(View):
    template_name = 'core/home.html'

    def get(self, request, *args, **kwargs):

        homepage_category = BookBelongsTo.objects.filter(slug='best-sellers').prefetch_related('homepagecategory').all()
        p = homepage_category[0].homepagecategory.select_related('author_name').all()
        bannerImg = Banner.objects.filter(is_active=True)
        ctx = {
            'title': 'Kitabalaya - Rent books in Nepal',
            'login_form': UserLoginForm(),
            'registration_form': RegistrationForm(),
            'home_books_category': p,
            'banners': bannerImg,
            'banner_first': bannerImg[0],
            'banner_range': range(len(bannerImg)),


            # 'session_id': request.session.get('card_id', None)
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
                    # 'book_rating': get_book_rating(book[0]),

                }
                return JsonResponse({'book': book_data}, status=200)

        return render(request, template_name='core/test.html', context={})


class SearchView(View):
    def post(self, request, *args, **kwargs):
        result = []

        q = request.POST.get('query')
        search_qs = Book.objects.filter(title__istartswith=q)[:10]

        for book in search_qs:
            result.append(book.title)

        # print(result)

        if request.is_ajax():
            return JsonResponse({'data': result}, status=200)

        return render(request, template_name='core/test.html', context={})


class Categories(View):
    template_name = 'core/categories.html'

    def get(self, request, *args, **kwargs):
        category = kwargs.get('slug', None)

        if category is not None:
            category_title = BookMainCategory.objects.get(slug=category)

            qs = BookMainCategory.objects.get(slug=category).book_set.all().select_related('author_name')
            language = Language.objects.all()

            sort_category = BookBelongsTo.objects.all()
            genre_in = Genre.objects.filter(belongs_to__slug=category)

            ctx = {
                'title': 'Categories',
                'all_books': qs,
                'genre_in': genre_in,
                'category_title': category_title,
                'languages': language,
                'sort_category': sort_category,
            }

            return render(request, template_name=self.template_name, context=ctx)


class FilterCategoryAPI(View):
    def get(self, request, *args, **kwargs):

        active_sub_genre = request.GET.get('genre')
        active_price_filter = request.GET.get('price')
        active_lang_filter = request.GET.get('lang')
        active_sort_filter = request.GET.get('sort')

        props = {
            'book_genre__slug': active_sub_genre,
            # 'mrp_price': active_price_filter,
            'language__slug': active_lang_filter,
            'homepage_category__slug': active_sort_filter,
        }

        if request.is_ajax:

            qs = Book.objects.filter(**props)
            print(qs)


            return JsonResponse({'success': 'success'})















