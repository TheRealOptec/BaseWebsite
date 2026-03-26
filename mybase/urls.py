from django.urls import path
from mybase import views

app_name = 'mybase'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('apis/', views.api_handler, name='api_handler'),
]