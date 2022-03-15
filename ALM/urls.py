from django.urls import path
from . import views

app_name = 'ALM'
urlpatterns = [
    path('', views.home, name='home'),
    path('area-personale', views.tempo_reale, name='tempo_reale'),
    path('chi-siamo', views.chi_siamo, name='chi_siamo'),
    path('il-nostro-servizio', views.il_nostro_servizio, name='il_nostro_servizio'),
    path('sostienici', views.sostienici, name='sostienici'),
    path('login', views.user_login, name='login'),
    path('register', views.user_register, name='user_register'),
]