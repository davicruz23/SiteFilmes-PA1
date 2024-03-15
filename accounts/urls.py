from django.urls import path
from accounts import views
from django.contrib.auth.views import LoginView

urlpatterns = [ 
    path('', views.register, name='register'), 
    path('accounts/logout/', views.logout, name='logout'),
    path('login/', LoginView.as_view(), name='login'),
] 