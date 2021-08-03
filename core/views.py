from django.contrib.auth import get_user_model
from django.db.models import Prefetch, Q, Avg
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, DetailView
from coreaccounts.forms import UserLoginForm, RegistrationForm
from corebookmodels.models import Book, Author, RentalCategory, Banner, BookBelongsTo, \
    BookMainCategory, BookCategory, Genre, Language, BookBelongsTo
from django.db import connection
from core.utils import get_obj_str, get_date_formatted, get_curr_url, get_cart_count, get_breadcrumbs, \
    get_filtered_book_serialized
import json
from django.core.paginator import Paginator
from django.core import serializers
from django.db.models import Q
from functools import reduce
import operator

from cart.utils import get_serialized
from django.core.paginator import Paginator


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
            paginate_qs = Paginator(qs, 9)
            page_number = request.GET.get('page')
            page_obj = paginate_qs.get_page(page_number)
            language = Language.objects.all()

            sort_category = BookBelongsTo.objects.all()
            genre_in = Genre.objects.filter(belongs_to__slug=category)

            ctx = {
                'title': 'Categories',
                'all_books': page_obj,
                'genre_in': genre_in,
                'category_title': category_title,
                'category': category,
                'languages': language,
                'sort_category': sort_category,
                'contain_genre_wrap': True,

            }

            return render(request, template_name=self.template_name, context=ctx)


class FilterCategoryAPI(View):
    def get(self, request, *args, **kwargs):

        active_sub_genre = request.GET.get('genre')
        active_price_filter = request.GET.get('price')
        active_lang_filter = request.GET.get('lang')
        active_sort_filter = request.GET.get('sort')
        active_main_category = request.GET.get('mainCategory')
        if active_sub_genre is None:
            active_sub_genre = request.GET.get('activeSubCategory').strip()
            if active_sub_genre == '':
                active_sub_genre = None

        props = {
            'book_main_category__slug': active_main_category,
            'book_genre__slug': active_sub_genre,
            'language__slug': active_lang_filter,
            'homepage_category__slug': active_sort_filter,
        }

        filtered = {k: v for k, v in props.items() if v is not None}
        props.clear()
        props.update(filtered)

        if request.is_ajax:
            qs = Book.objects.filter(**props)
            if active_price_filter == 'ltoh':
                qs = qs.order_by("mrp_price")
            if active_price_filter == 'htol':
                qs = qs.order_by("-mrp_price")

            paginate_qs = Paginator(qs, 9)
            page_number = request.GET.get('page_number')
            page_obj = paginate_qs.get_page(page_number)

            filtered_books = get_filtered_book_serialized(page_obj)
            next_page = None

            if page_obj.has_next():
                next_page = page_obj.next_page_number()
            else:
                next_page = 0
            print('...................')
            print(page_obj.has_next())
            print(next_page)

            return JsonResponse({'filtered_books': filtered_books,'next_page': next_page,'success': 'success'}, status=200)


class SubCategoryView(View):
    def get(self, request, *args, **kwargs):
        try:
            cat_obj = BookMainCategory.objects.get(slug=kwargs['mainCategory'])
            sub_cat_slug = kwargs['subCategory']
            related_sub_genre = cat_obj.genre_set.all()
            language = Language.objects.all()

            sort_category = BookBelongsTo.objects.all()

            qs = Book.objects.filter(book_main_category=cat_obj, book_genre__slug=sub_cat_slug).select_related('author_name')

            paginate_qs = Paginator(qs, 9)
            page_number = request.GET.get('page_number')
            page_obj = paginate_qs.get_page(page_number)

        except BookMainCategory.DoesNotExist:
            return redirect('home')

        if request.is_ajax():
            filtered_books = get_filtered_book_serialized(page_obj)

            return JsonResponse({'filtered_books': filtered_books,'success': 'success'}, status=200)

        ctx = {
            'related_genre': related_sub_genre,
            'languages': language,
            'sort_category': sort_category,
            'main_category': cat_obj,
            'sub_category': sub_cat_slug,
            'qs': page_obj,
            'category':kwargs['mainCategory'],


        }

        return render(request, template_name='core/sub-category.html', context=ctx)

    # def post(self, request, *argsm, **kwargs):
    #     return render(request, template_name='core/test.html')










