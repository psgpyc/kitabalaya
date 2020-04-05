from django.contrib import admin
from corebookmodels.models import Language, Author, Book, Publication, Genre, Nationality

admin.site.register(Language)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Publication)
admin.site.register(Genre)
admin.site.register(Nationality)
