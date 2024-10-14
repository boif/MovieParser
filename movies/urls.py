from django.urls import path
from movies.views import load_movies, movies_view

urlpatterns = [
    path('', movies_view, name='movies_view'),
    path('load_movies/', load_movies, name='load_movies'),
]
