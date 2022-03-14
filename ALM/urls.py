from django.urls import path
from . import views

app_name = 'ALM'
urlpatterns = [
    path('', views.home, name='home'),
    path('area-personale', views.tempo_reale, name='tempo_reale'),
    path('login', views.user_login, name='login'),
    path('register', views.user_register, name='user_register'),
]