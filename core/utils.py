from corebookmodels.models import BookRatingModel
from django.db.models import Avg, Q
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format


def get_obj_str(obj):
    obj_str = ' '
    for i in obj:
        obj_str += str(i)+', '
    return obj_str


def get_book_rating(obj):
    rating = BookRatingModel.objects.filter(book=obj).aggregate(Avg('rating'))['rating__avg']
    rating_count = BookRatingModel.objects.filter(book=obj).count()
    print('Book rating:{}'.format(rating_count))

    if rating is None:
        rating = 0

    return round(rating, 1)


def get_my_rating(book, user):
    try:
        my_rating = BookRatingModel.objects.get(Q(created_by=user) & Q(book=book))
    except BookRatingModel.DoesNotExist:
        my_rating = 0
        return my_rating

    return my_rating.rating


def get_date_formatted(obj):
    df = DateFormat(obj.published_date)
    df.format(get_format('DATE_FORMAT'))
    print(df.format(get_format('DATE_FORMAT')))
    return df.format(get_format('DATE_FORMAT'))
