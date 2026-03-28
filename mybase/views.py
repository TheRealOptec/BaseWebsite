from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from mybase.forms import PostForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

from mybase.models import Topic,Page,User,UserProfile,Comment,PostLike,TopicHistory,PostHistory

from .apis.api_handler import ApiHandler
from .searching.searching_handler import SearchingHandler
from .searching.search_in_options import SearchIn
from .searching.sort_by_options import SortBy


def _get_topic(topic_slug):
    try:
        return Topic.objects.get(slug=topic_slug)
    except Topic.DoesNotExist:
        return None


def _get_post(topic, post_slug):
    try:
        return Page.objects.get(topic=topic, slug=post_slug)
    except Page.DoesNotExist:
        return None


def _render_post_form(request, topic, post_form, post=None):
    return render(request, 'mybase/make_post.html', context={
        "topic": topic,
        "post": post,
        "post_form": post_form,
        "is_editing": post is not None,
    })

def redirect_home(request):
    return redirect(reverse("mybase:home"))

def home(request):
    # Get recent topics and posts
    if request.user.is_authenticated:
        recent_topics = [x.topic for x in TopicHistory.objects.filter(user=request.user).order_by("-access_time")]
        recent_posts = [x.post for x in PostHistory.objects.filter(user=request.user).order_by("-access_time")]
    else:
        recent_topics = []
        recent_posts = []
    # Get most viewed and most liked topics
    most_viewed_topic = Topic.objects.order_by("-likes")[0]
    most_liked_topic = Topic.objects.order_by("-views")[0]
    # Render home page
    context_dict = {
        "static_css_path": settings.STATIC_CSS_URL,
        "recent_topics": recent_topics,
        "recent_posts": recent_posts,
        "most_viewed_topic": most_viewed_topic,
        "most_liked_topic": most_liked_topic
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
    try:
        user_profile = UserProfile.objects.get(slug=username_slug)
        user = user_profile.user
    except:
        user_profile = None
        user = None
    return render(request, 'mybase/profile.html', context={
        "profile": user_profile,
        "profile_user": user
    })

def view_post(request, topic_slug, post_name_slug):
    # Get this topic and post
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
    # Increase view counts
    post.views += 1
    post.save()
    # Add post history (if valid)
    if request.user.is_authenticated:
        post_history = PostHistory(user=request.user, post=post)
        post_history.save()
    # If comment is being added then add comment
    if request.method == "POST":
        # Got help from: https://forum.djangoproject.com/t/how-to-get-current-user/10234/5
        comment = Comment(author=request.user, post=post, body=request.POST.get("body", ""))
        comment.save()
    try:
        comments = Comment.objects.filter(post=post).values()
    except:
        comments = None
    post.user_has_liked = False
    if request.user.is_authenticated:
        post.user_has_liked = PostLike.objects.filter(user=request.user, post=post).exists()
    return render(request, 'mybase/post_detail.html', context={
        "post": post,
        "comments": comments
    })

@login_required(login_url='/login/')
def like_post(request, topic_slug, post_name_slug):
    if request.method != "POST":
        return redirect(reverse("mybase:view_topic", args=[topic_slug]))

    try:
        topic = Topic.objects.get(slug=topic_slug)
        post = Page.objects.get(topic=topic, slug=post_name_slug)
        existing_like = PostLike.objects.filter(user=request.user, post=post).first()
        if existing_like:
            existing_like.delete()
        else:
            PostLike.objects.create(user=request.user, post=post)
        post.likes = PostLike.objects.filter(post=post).count()
        post.save(update_fields=['likes'])
    except:
        return redirect(reverse("mybase:home"))

    next_url = request.POST.get("next", "")
    if next_url.startswith('/'):
        return redirect(next_url)

    return redirect(reverse("mybase:view_post", args=[topic_slug, post_name_slug]))

def view_topic(request, topic_slug):
    # Attempt to get the topic from the slug
    try:
        topic = Topic.objects.get(slug=topic_slug)
    except:
        topic = None
    # If a topic was found
    if topic is not None:
        # Add a view
        topic.views += 1
        topic.save()
        # Add topic history to user (if valid)
        if request.user.is_authenticated:
            topic_history = TopicHistory(topic=topic, user=request.user)
            topic_history.save()
        # Get posts as list
        posts = list(Page.objects.filter(topic=topic).values())

        # Get likes
        if request.user.is_authenticated:
            # Set whether or not the user has liked the post
            for post in posts:
                post["user_has_liked"] = PostLike.objects.filter(user=request.user, post=post["id"]).exists()
        return render(request, 'mybase/topic.html', context={
            "topic": topic,
            "posts": posts
        })
    # TODO - change this
    return HttpResponse("Invalid topic")

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
    topic = _get_topic(topic_slug)
    if topic is None:
        return redirect(reverse('mybase:home'))

    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            if Page.objects.filter(topic=topic).exists():
                post_form.add_error(None, "This topic already has a post and cannot accept another one right now.")
            elif Page.objects.filter(author=request.user).exists():
                post_form.add_error(None, "Your account already has a post and cannot create another one right now.")
            else:
                post = Page(
                    topic=topic,
                    author=request.user,
                    title=post_form.cleaned_data['title'],
                    body=post_form.cleaned_data['body'],
                )
                post.save()
                return redirect(reverse('mybase:view_post', args=[topic.slug, post.slug]))
    else:
        post_form = PostForm()

    return _render_post_form(request, topic, post_form)


@login_required
def edit_post(request, topic_slug, post_name_slug):
    topic = _get_topic(topic_slug)
    if topic is None:
        return HttpResponse("No such topic exist", status=404)

    post = _get_post(topic, post_name_slug)
    if post is None:
        return HttpResponse("No such post exists", status=404)

    if post.author != request.user:
        return HttpResponse("You do not have permission to edit this post.", status=403)

    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post.title = post_form.cleaned_data['title']
            post.body = post_form.cleaned_data['body']
            post.save()
            return redirect(reverse('mybase:view_post', args=[topic.slug, post.slug]))
    else:
        post_form = PostForm(initial={
            "title": post.title,
            "body": post.body,
        })

    return _render_post_form(request, topic, post_form, post=post)

def api_handler(request):
    return ApiHandler.handleReq(request)

def posting_guide(request):
    return render(request, 'mybase/posting_guide.html', context={})

def toggle_like_post(request, topic_slug, post_slug):
    # Ensure that this is a POST request - otherwise let it return a 404 not found
    if request.method == "POST":
        # Ensure user is authenticated
        if request.user.is_authenticated:
            # Attempt to get the the topic and post
            try:
                topic = Topic.objects.get(slug=topic_slug)
            except:
                # TODO - change this later
                return HttpResponse("Invalid topic")
            try:
                post = Page.objects.get(slug=post_slug, topic=topic)
            except:
                # TODO - change this later
                return HttpResponse("Invalid post")
            # Toggle the likes - (could use get_or_create here to simplify logic)
            try:
                pl = PostLike.objects.get(user=request.user, post=post, topic=topic)
                # If liked vvv
                pl.delete() # Please don't explode things
            except:
                # If not liked vvv
                pl = PostLike(user=request.user, post=post, topic=topic)
                pl.save()
            # TODO - also change this to a reverse
            return redirect(f"/mybase/topic/{topic.slug}/")
