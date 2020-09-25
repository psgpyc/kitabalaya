from corebookmodels.models import BookMainCategory


def get_categories(request):
    qs = BookMainCategory.objects.prefetch_related('main_category').all()
    ctx = {
        'categories': qs,
    }
    return ctx
