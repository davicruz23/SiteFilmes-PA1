from django.urls import path 
from myapp import views

urlpatterns = [
    path('', views.home, name='index'),
    path('perfil/<str:username>/', views.exibir_perfil_usuario, name='perfil_usuario'),
    path('browse/', views.browse, name='browse'),
    path('details/<int:filme_id>/', views.filme_details, name='filme_details'),
    path('streams/', views.streams, name='streams'),
    path('profile/', views.profile, name='profile'),
    path('video-list/', views.video_list, name='video_list'),
    path('search/', views.search_movies, name='search_movies'),
    path('profile-edit/', views.update_profile, name='atualizar_perfil'),
    path('marcar_visto/<int:filme_id>/', views.marcar_visto, name='marcar_visto'),
]
