from django.urls import path 
from myapp import views

urlpatterns = [
    path('', views.mysite, name='index'),
    path('browse/', views.browse, name='browse'),
    path('details/', views.details, name='details'),
    path('streams/', views.streams, name='streams'),
    path('profile/', views.profile, name='profile'),
    path('video-list/', views.video_list, name='video_list'),
    path('search/', views.search_movies, name='search_movies'),
]
