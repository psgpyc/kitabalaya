from core.utils import get_cart_count, get_cart_items
from corebookmodels.models import BookMainCategory


def get_categories(request):
    qs = BookMainCategory.objects.prefetch_related('main_category').all()
    cart_product_count = get_cart_count(request)
    ctx = {
        'categories': qs,
        'cart_product_count': cart_product_count,
        # 'cart_items': get_cart_items(request),
    }
    return ctx
