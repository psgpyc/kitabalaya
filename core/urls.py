from django.urls import path, include, re_path

from core.views import Home, BookDetails, SearchView, Categories, FilterCategoryAPI, SubCategoryView

urlpatterns = (
    path('', Home.as_view(), name='home'),
    path('ajax/search/', SearchView.as_view(), name='search-view'),
    path('book/<slug:slug>/', BookDetails.as_view(), name='book-details'),
    # path('rating/<slug:slug>/', UpdateBookRating.as_view(), name='update-book-rating')
    path('ajax/get_filtered/', FilterCategoryAPI.as_view(), name='get-filtered'),


)
