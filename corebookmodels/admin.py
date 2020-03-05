from django.contrib import admin
from corebookmodels.models import Language, Author, Book, Publication, Genre

admin.site.register(Language)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Publication)
admin.site.register(Genre)
