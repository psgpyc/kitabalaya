from django.db import models
from corebookmodels.abstractmodels import TimeStampModel
from corebookmodels.models import Book
from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed, pre_save
from django.db import connection, reset_queries

User = get_user_model()


class CartManager(models.Manager):

    def create_or_get(self, request):
        reset_queries()
        cart_id = request.session.get('cart_id', None)

        qs = self.get_queryset().filter(id=cart_id).select_related('user')

        if len(qs) == 1:
            created = False
            cart_obj = qs[0]

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
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    sub_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    refundable = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


class CartItemManager(models.Manager):
    def create_get(self, product, belongs_to, rent_or_buy):
        created = False
        if rent_or_buy is None:
            rent_or_buy = 'BUY'
        cart_product = self.get_queryset().filter(belongs_to=belongs_to,product=product, rent_or_buy=rent_or_buy).select_related('product__author_name')
        if len(cart_product) == 1:
            created = False
            return cart_product, created

        else:
            created = True
            return self.create(belongs_to=belongs_to, product=product, rent_or_buy=rent_or_buy), created

    def cart_item_remove(self, product, belongs_to, rent_or_buy):
        deleted = False
        cart_item = self.filter(product=product, belongs_to=belongs_to, rent_or_buy=rent_or_buy)
        if cart_item.exists() and len(cart_item) == 1:
            print('coming in')
            cart_item.delete()
            deleted = True

        return deleted


class CartItem(models.Model):

    class RentBuyChoices(models.TextChoices):
        RENT = 'RNT', 'RENT'
        BUY = 'BUY', 'BUY'

    belongs_to = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    rent_or_buy = models.CharField(max_length=3, choices=RentBuyChoices.choices, default=RentBuyChoices.BUY)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = CartItemManager()

    def __str__(self):
        return f'{str(self.belongs_to.id)}-{self.product.slug}'

    def get_product_quantity(self):
        return self.quantity

    def get_rent_or_buy(self):
        return self.rent_or_buy


# def cart_product_update_receiver(sender, instance, action, *args, **kwargs):
#     if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
#         qs = instance.products.all()
#         sub_total = 0
#         sub_total = sum([eachProduct.mrp_price for eachProduct in instance.products.all()])
#         # if instance.sub_total != instance.total:
#         instance.sub_total = sub_total
#         instance.save()
#
#
# m2m_changed.connect(cart_product_update_receiver, sender=Cart.products.through)
#
#
# def pre_save_cart_receiver(sender, instance, *args, **kwargs):
#     if instance.sub_total > 0:
#         instance.total = instance.sub_total
#     else:
#         instance.total = 0.00
#
#
# pre_save.connect(pre_save_cart_receiver, sender=Cart)
