from django.urls import path 
from myapp import views

urlpatterns = [
    path('', views.mysite, name='index'),
    path('browse/', views.browse, name='browse'),
    path('details/', views.details, name='details'),
    path('streams/', views.streams, name='streams'),
]
