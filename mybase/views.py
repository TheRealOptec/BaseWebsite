from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from mybase.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

from mybase.models import Topic,Page,User,UserProfile

from .apis.api_handler import ApiHandler
from .searching.searching_handler import SearchingHandler
from .searching.search_in_options import SearchIn
from .searching.sort_by_options import SortBy

def home(request):
    context_dict = {
        "static_css_path": settings.STATIC_CSS_URL
    }
    return render(request, 'mybase/home.html', context=context_dict)

def search(request):
    query = request.GET.get("q", None)
    # If blank or not provided then redirect back to the home page
    if query is None or query == "":
        return redirect(reverse("mybase:home"))
    # Get filtering options
    searchIn = SearchIn.fromStr(request.GET.get("search_in", "all"))
    sortBy = SortBy.fromStr(request.GET.get("sort_by", "most_liked"))
    (post_results, topic_results) = SearchingHandler.search(q=query, searchIn=searchIn, sortBy=sortBy)
    context_dict = {
        "query": query,
        "post_results": post_results,
        "topic_results": topic_results
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

def sign_up_v2(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        email = request.POST.get("email", None)
        password1 = request.POST.get("password1", None)
        password2 = request.POST.get("password2", None)
        # Check data validity
        if (password1 is None or password2 is None or email is None or username is None):
            print("A field is invalid on sign_up_v2")
            return render(request, "mybase/sign_up.html", context={})
        # Check if the password has been confirmed properly
        if (password1 != password2):
            # TODO - try and do this dynamically if possible, I believe we could use Ajax for this
            return HttpResponse("Did not confirm password")
        # Sign in and render new home page
        user = User(username=username, email=email, password=password1)
        user.save()
        userProfile = UserProfile(user=user)
        userProfile.save()
        login(request, user)
        return redirect(reverse("mybase:home"))
        
    return render(request, "mybase/sign_up.html", context={})

def user_login(request):
    invalid_details = False
    account_disabled = False
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse("mybase:home"))
            else:
                account_disabled = True
        else:
            invalid_details = True
    return render(request, 'mybase/login.html', context={
        "invalid_details": invalid_details,
        "account_disabled": account_disabled
    })

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('mybase:home'))

@login_required
def edit_user_profile(request):
    return render(request, 'mybase/edit_profile.html', context={})

def view_profile(request, username_slug):
    # TODO - db query here
    return render(request, 'mybase/profile.html', context={})

def view_post(request, topic_slug, post_name_slug):
    try:
        topic = Topic.objects.get(slug=topic_slug)
    except:
        # TODO - remove this
        return HttpResponse("No such topic exist")
    try:
        post = Page.objects.get(topic=topic, slug=post_name_slug)
    except:
        # TODO - remove this
        return HttpResponse("No such post exists")
    return render(request, 'mybase/post_detail.html', context={
        "post": post
    })

def view_topic(request, topic_slug):
    try:
        topic = Topic.objects.get(slug=topic_slug)
    except:
        topic = None
    posts = Page.objects.filter(topic=topic).values()
    return render(request, 'mybase/topic.html', context={
        "topic": topic,
        "posts": posts
    })

@login_required
def make_topic(request):
    # Adapted code from: https://www.w3schools.com/django/django_insert_data.php
    if request.method == "POST":
        topic_name = request.POST.get("name", None)
        if topic_name is None:
            # TODO - could change this
            return redirect(reverse('mybase:make_topic'))
        topic_description = request.POST.get("description", "")
        topic = Topic(name=topic_name, description=topic_description)
        topic.save()
        # TODO - change this to a reverse
        return redirect(f"/mybase/topic/{topic_name}/")
    return render(request, 'mybase/make_topic.html', context={})

@login_required
def make_post(request, topic_slug):
    if request.method == "POST":
        try:
            topic = Topic.objects.get(slug=topic_slug)
        except:
            # TODO - remove this
            return redirect(reverse('mybase:home'))
        post = Page(
            topic=topic,
            title=request.POST.get('title', None),
            body=request.POST.get('body', "")
        )
        post.save()
        return render(request, 'mybase/make_post.html', context={
            "topic": topic
        })
    try:
        topic = Topic.objects.get(slug=topic_slug)
    except:
        topic = None
    return render(request, 'mybase/make_post.html', context={
        "topic": topic
    })

def api_handler(request):
    return ApiHandler.handleReq(request)

def posting_guide(request):
    return render(request, 'mybase/posting_guide.html', context={})