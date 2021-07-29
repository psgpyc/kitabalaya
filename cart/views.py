from django.shortcuts import render
from django.views.generic import View

from cart.utils import get_serialized
from corebookmodels.models import Book
from django.core import serializers

from cart.models import Cart, CartItem
from django.db import connection, reset_queries
from django.http import JsonResponse
from core.utils import get_cart_count


class InitCart(View):

    template_name = 'core/test.html'

    def get(self, request):

        cart_obj, created = Cart.objects.create_or_get(request)

        return render(request, template_name=self.template_name, context={'cart_id': cart_obj.id, 'cart_user':cart_obj.user, 'created': created})


class UpdateCart(View):
    def post(self, request, *args, **kwargs):
        cart_id, created = Cart.objects.create_or_get(request)
        print('passed through')
        if request.is_ajax:

            product_slug = request.POST.get('productSlug', None)
            order_type = request.POST.get('orderType', None)
            if product_slug:
                product = Book.objects.get_book(slug=product_slug)
                if len(product) == 1:
                    cart_item, created = CartItem.objects.create_get(belongs_to=cart_id, product=product[0], rent_or_buy=order_type)
                    print(f'connection:{len(connection.queries)}')

                    if created is False and cart_item.exists():
                        cart_item = cart_item.first()
                        if cart_item.rent_or_buy == 'RNT':
                            return JsonResponse({'created': 'Rent False'}, status=200)
                        cart_item.quantity += 1
                        cart_item.save()

                        cart_item = {
                            'slug': cart_item.product.slug,
                            'rent_or_buy': cart_item.rent_or_buy,
                            'quantity': cart_item.quantity,
                            'mrp_price': int(cart_item.product.mrp_price),
                            'cart_product_count': get_cart_count(request),

                        }
                        print(f'connection:{len(connection.queries)}')

                        return JsonResponse({'cart_item': cart_item, 'created': 'false'}, status=200)
                    if created is True:
                        cart_item.save()
                        book = {
                            'title': cart_item.product.title,
                            'author_name': cart_item.product.author_name.name,
                            'book_image': cart_item.product.book_image.url,
                            'mrp_price': int(cart_item.product.mrp_price),
                            'book_slug': cart_item.product.slug,
                            'cart_product_count': get_cart_count(request),
                            'rent_or_buy': cart_item.rent_or_buy,
                            'quantity': cart_item.quantity,


                        }
                        print(f'connection:{len(connection.queries)}')

                        return JsonResponse({'book': book, 'created':'true'}, status=200)

        return render(request, template_name='core/test.html', context={})


class DisplayCart(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax:
            cart_id = request.session.get('cart_id', None)
            if cart_id is None:
                return JsonResponse({'cart_obj': 0}, status=200)
            if cart_id is not None and get_cart_count(request) == 0:
                return JsonResponse({'cart_obj': 0}, status=200)
            else:
                cart_obj = Cart.objects.get(id=cart_id)
                ser_list = get_serialized(cart_obj.cart_item.select_related('product').select_related('product__author_name'))
                return JsonResponse({'data': ser_list}, status=200)

        return render(request, template_name='core/test.html', context={})

    def post(self, request, *args, **kwargs):
        book_slug = request.POST.get('book_slug', None)
        cart_id = request.session.get('cart_id', None)
        order_type = request.POST.get('orderType', None)
        print(book_slug, cart_id, order_type)
        if book_slug is not None and cart_id is not None:
            if request.is_ajax:
                book_obj = Book.objects.get(slug=book_slug)
                cart_obj = Cart.objects.get(id=cart_id)

                deleted = CartItem.objects.cart_item_remove(product=book_obj, belongs_to=cart_obj, rent_or_buy=order_type)

                if deleted is True:
                    return JsonResponse({'data':'success', 'cart_product_count': get_cart_count(request)}, status=200)

        return render(request, template_name='core/test.html', context={})