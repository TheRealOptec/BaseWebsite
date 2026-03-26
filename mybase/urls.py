from django.urls import path
from mybase import views

app_name = 'mybase'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('apis/', views.api_handler, name='api_handler'),
    path('login/', views.user_login, name='login'),
]