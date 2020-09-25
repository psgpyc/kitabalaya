from django.urls import path, include, re_path

from core.views import Home, BookDetails, UpdateBookRating

urlpatterns = (
    path('', Home.as_view(), name='home'),
    path('<slug:slug>/', BookDetails.as_view(), name='book-details'),
    path('rating/<slug:slug>/', UpdateBookRating.as_view(), name='update-book-rating')

)
