from django.db import models
from corebookmodels.abstractmodels import TimeStampModel
from corebookmodels.models import Book
from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed, pre_save

User = get_user_model()


class CartManager(models.Manager):

    def create_or_get(self, request):
        cart_id = request.session.get('cart_id', None)

        qs = self.get_queryset().filter(id=cart_id)

        if qs.exists() and qs.count() == 1:
            created = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
            print('cart exists')

        else:
            cart_obj = self.cart_create(user=request.user)
            created = True
            request.session['cart_id'] = cart_obj.id
            print('cart created')

        return cart_obj, created

    def cart_create(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    products = models.ManyToManyField(Book, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    sub_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = CartManager()


    def __str__(self):
        return str(self.id)


def cart_product_update_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        qs = instance.products.all()
        sub_total = 0
        sub_total = sum([eachProduct.mrp_price for eachProduct in instance.products.all()])
        # if instance.sub_total != instance.total:
        instance.sub_total = sub_total
        instance.save()


m2m_changed.connect(cart_product_update_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.sub_total > 0:
        instance.total = instance.sub_total
    else:
        instance.total = 0.00





pre_save.connect(pre_save_cart_receiver, sender=Cart)
