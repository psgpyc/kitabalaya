from django.shortcuts import render
from django.views.generic import View

from cart.models import Cart


class InitCart(View):

    template_name = 'core/test.html'

    def get(self, request):

        cart_obj, created = Cart.objects.create_or_get(request)

        return render(request, template_name=self.template_name, context={'cart_id': cart_obj.id, 'cart_user':cart_obj.user, 'created': created})


class UpdateCart(View):
    def post(self, request):
        pass
