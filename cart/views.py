from django.shortcuts import render
from django.views.generic import View

from cart.utils import get_serialized
from corebookmodels.models import Book
from django.core import serializers

from cart.models import Cart
from django.db import connection, reset_queries
from django.http import JsonResponse
from core.utils import get_cart_count


class InitCart(View):

    template_name = 'core/test.html'

    def get(self, request):

        cart_obj, created = Cart.objects.create_or_get(request)

        return render(request, template_name=self.template_name, context={'cart_id': cart_obj.id, 'cart_user':cart_obj.user, 'created': created})


class UpdateCart(View):
    def post(self, request):
        cart_id, created = Cart.objects.create_or_get(request)
        print(cart_id)
        if request.is_ajax:

            product_slug = request.POST.get('productSlug', None)
            if product_slug:
                product = Book.objects.get_book(slug=product_slug)
                if product.exists() and product.count() == 1:
                    product = product[0]
                    cart_id.products.add(product)
                    cart_id.save()
                    book = {
                        'title' : product.title,
                        'author_name': product.author_name.name,
                        'book_image': product.book_image.url,
                        'mrp_price': product.mrp_price,
                        'cart_product_count': get_cart_count(request)

                    }

                    return JsonResponse({'book': book}, status=200)

        return render(request, template_name='core/test.html', context={})


class DisplayCart(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax:
            cart_id = request.session.get('cart_id', None)
            if cart_id is None:
                return JsonResponse({'cart_obj': 0}, status=200)
            else:
                cart_obj = Cart.objects.get(id=cart_id)
                ser_list = get_serialized(cart_obj.products.all())
                return JsonResponse({'data': ser_list}, status=200)

        return render(request, template_name='core/test.html', context={})