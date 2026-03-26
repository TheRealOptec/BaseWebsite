from django.urls import path
from mybase import views

app_name = 'mybase'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('apis/', views.api_handler, name='api_handler'),
    path('make-topic/', views.make_topic, name='make_topic'),
    path('topic/<slug:topic_slug>/', views.view_topic, name='view_topic'),
    path('topic/<slug:topic_slug>/post/<slug:post_name_slug>', views.view_post, name='view_post'),
    path('topic/<slug:topic_slug>/make-post/', views.make_post, name='make_post'),
]