from cart.models import Cart
from django.db.models import Avg, Q
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format


def get_obj_str(obj):
    obj_str = ' '
    for i in obj:
        obj_str += str(i)+', '
    return obj_str


# def get_book_rating(obj):
#     rating = BookRatingModel.objects.filter(book=obj).aggregate(Avg('rating'))['rating__avg']
#
#     if rating is None:
#         rating = 0
#
#     return round(rating, 1)
#
#
# def get_my_rating(book, user):
#     try:
#         my_rating = BookRatingModel.objects.get(Q(created_by=user) & Q(book=book))
#     except BookRatingModel.DoesNotExist:
#         my_rating = 0
#         return my_rating
#
#     return my_rating.rating


def get_date_formatted(obj):
    df = DateFormat(obj.published_date)
    df.format(get_format('DATE_FORMAT'))
    return df.format(get_format('DATE_FORMAT'))


def get_curr_url(a):

    b = a.split('/')

    return b


def get_cart_items(request):
    cart_id = request.session.get('cart_id', None)

    if cart_id:
        cart = Cart.objects.filter(id=cart_id)
        if cart:
            cart = cart.first()
            return cart.cart_item.select_related('product')
        else:
            return []
    else:
        return []


def get_cart_count(request):
    cart_items = get_cart_items(request)
    cart_length = 0

    if len(cart_items) != 0:
        for eachBook in cart_items:
            cart_length+=eachBook.quantity

        return cart_length

    if len(cart_items) == 0:
        return 0


