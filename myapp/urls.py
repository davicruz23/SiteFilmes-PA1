from django.urls import path 
from myapp import views

urlpatterns = [
    path('', views.mysite, name='index'),
    path('browse/', views.browse, name='browse'),
    path('details/<int:filme_id>/', views.filme_details, name='filme_details'),
    path('streams/', views.streams, name='streams'),
    path('profile/', views.profile, name='profile'),
    path('video-list/', views.video_list, name='video_list'),
    path('search/', views.search_movies, name='search_movies'),
    path('profile-edit/', views.update_profile, name='atualizar_perfil'),
    path('filme/<int:filme_id>/add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),

]
