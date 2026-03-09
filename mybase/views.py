from django.shortcuts import render, redirect
from django.conf import settings

def index(request):
    context_dict = {
        "static_css_path": settings.STATIC_CSS_URL
    }
    return render(request, 'mybase/base.html', context=context_dict)
