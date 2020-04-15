from django.db import models
from django.contrib.auth import get_user_model
from corebookmodels.models import Book

User = get_user_model()


class SubscribedBook(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    book = models.OneToOneField(Book, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{book} {user}'.format(book=self.book.title, user=self.user.name)


