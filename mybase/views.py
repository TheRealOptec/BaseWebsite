from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from mybase.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

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

def sign_up(request):

    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # Add profile picture
            if 'pfp' in request.FILES:
                profile.pfp = request.FILES['pfp']
            
            # This causes an error and I'm not sure why
            #profile.save()
            return redirect(reverse("mybase:home"))
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, "mybase/sign_up.html", context={
        "user_form": user_form,
        "profile_form": profile_form
    })

def user_login(request):
    print(f"I'm usering it: {request.method}")
    if request.method == "POST":
        print("Posting")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse("mybase:home"))
            else:
                return HttpResponse("Your account has been disabled")
        else:
            return HttpResponse("Invalid login details suplied")
    return render(request, 'mybase/login.html', context={  })

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('mybase:home'))

def api_handler(request):
    return ApiHandler.handleReq(request)