from django.urls import path
from . import views

urlpatterns = [
    path('countries/', views.country_list, name='country_list'),
    path('countries/<str:cca3>/', views.country_detail, name='country_detail'),
    path('stats/', views.stats, name='stats'),
    path('', views.country_list, name='home'),
]
