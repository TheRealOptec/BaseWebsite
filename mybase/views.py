from django.shortcuts import render, redirect
from django.conf import settings

from .apis.api_handler import ApiHandler

def home(request):
    context_dict = {
        "static_css_path": settings.STATIC_CSS_URL
    }
    return render(request, 'mybase/home.html', context=context_dict)

def search(request):
    context_dict = {
        "query": request.GET.get("q", None)
    }
    return render(request, 'mybase/search.html', context=context_dict)

def api_handler(request):
    return ApiHandler.handleReq(request)