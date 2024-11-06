# example/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('login/', views.spotify_login, name="spotify_login"),
    path('callback/', views.spotify_callback, name='spotify_callback'),
    path('re-auth/', views.reauthenticate, name="reauthenticate"),
    path('search_track/', views.search_track, name="search_track"),
    path('get_features/', views.get_several_features, name="get_several_features"),
]