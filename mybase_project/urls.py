"""mybase_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mybase import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mybase/', include('mybase.urls')),
    path('sign-up/', views.sign_up_v2, name='sign_up'),
    path('logout/', views.user_logout, name='user_logout'),
    path('login/', views.user_login, name='user_login'),
    path('edit-profile/', views.edit_user_profile, name='edit_user_profile'),
    path('view-profile/<slug:username_slug>/', views.view_profile, name='view_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
