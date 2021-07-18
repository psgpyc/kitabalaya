from django.contrib import admin
from corebookmodels.models import (
    Language,
    Author,
    Book,
    Publication,
    Genre,
    Nationality,
    RentalCategory,
    BookMainCategory,
    BookCategory,
    Banner,
    BookBelongsTo
    )

admin.site.register(Language)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Publication)
admin.site.register(Genre)
admin.site.register(Nationality)
admin.site.register(RentalCategory)
admin.site.register(BookMainCategory)
admin.site.register(BookCategory)
admin.site.register(Banner)
admin.site.register(BookBelongsTo)
