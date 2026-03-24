from django.shortcuts import render, redirect
from django.conf import settings

from .apis.api_handler import ApiHandler

def index(request):
    context_dict = {
        "static_css_path": settings.STATIC_CSS_URL
    }
    return render(request, 'mybase/base.html', context=context_dict)

def api_handler(request):
    return ApiHandler.handleReq(request)