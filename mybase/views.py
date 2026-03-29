from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from mybase.forms import (
    CommentForm,
    LoginForm,
    PostForm,
    SignUpForm,
    TopicForm,
    UserAccountForm,
    UserProfileEditForm,
)
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


def _render_sign_up(request, user_form):
    return render(request, "mybase/sign_up.html", context={
        "user_form": user_form,
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
    most_viewed_topic = Topic.objects.order_by("-views")[0]
    most_liked_topic = Topic.objects.order_by("-likes")[0]
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
    return sign_up_v2(request)

def sign_up_v2(request):
    user_form = SignUpForm(request.POST or None)

    if request.method == "POST" and user_form.is_valid():
        user = user_form.save()
        UserProfile.objects.get_or_create(user=user)

        authenticated_user = authenticate(
            username=user.username,
            password=user_form.cleaned_data["password1"],
        )
        if authenticated_user is not None:
            login(request, authenticated_user)
        return redirect(reverse("mybase:home"))

    return _render_sign_up(request, user_form)

def user_login(request):
    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())

        next_url = request.POST.get("next") or request.GET.get("next", "")
        if next_url.startswith('/'):
            return redirect(next_url)

        return redirect(reverse("mybase:home"))

    return render(request, 'mybase/login.html', context={
        "form": form,
    })

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('mybase:home'))

@login_required
def edit_user_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = UserAccountForm(request.POST, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            saved_profile = profile_form.save(commit=False)
            saved_profile.user = user
            saved_profile.save()
            return redirect(reverse("view_profile", args=[user.username]))
    else:
        user_form = UserAccountForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=profile)

    return render(request, 'mybase/edit_profile.html', context={
        "profile": profile,
        "user_form": user_form,
        "profile_form": profile_form,
    })

def view_profile(request, username):
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist | User.DoesNotExist:
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
    comment_form = CommentForm()

    # Increase view counts
    post.views += 1
    post.save()
    # Add post history (if valid)
    if request.user.is_authenticated:
        post_history = PostHistory(user=request.user, post=post)
        post_history.save()
    # If comment is being added then add comment
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if request.user.is_authenticated and comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            comment_form = CommentForm()
    comments = Comment.objects.filter(post=post).select_related("author").order_by("-created_at")
    post.user_has_liked = False
    if request.user.is_authenticated:
        post.user_has_liked = PostLike.objects.filter(user=request.user, post=post).exists()
    return render(request, 'mybase/post_detail.html', context={
        "post": post,
        "comments": comments,
        "comment_form": comment_form,
    })

@login_required(login_url='/login/')
def like_post(request, topic_slug, post_name_slug):
    if request.method != "POST":
        return redirect(reverse("mybase:view_topic", args=[topic_slug]))

    try:
        topic = Topic.objects.get(slug=topic_slug)
        post = Page.objects.get(topic=topic, slug=post_name_slug)
        existing_like = PostLike.objects.filter(user=request.user, post=post, topic=topic).first()
        if existing_like:
            existing_like.delete()
        else:
            PostLike.objects.create(user=request.user, post=post, topic=topic)
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
    topic_form = TopicForm(request.POST or None)

    if request.method == "POST" and topic_form.is_valid():
        topic = topic_form.save()
        return redirect(reverse("mybase:view_topic", args=[topic.slug]))

    return render(request, 'mybase/make_topic.html', context={
        "topic_form": topic_form,
    })

@login_required
def make_post(request, topic_slug):
    topic = _get_topic(topic_slug)
    if topic is None:
        return redirect(reverse('mybase:home'))

    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
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
    if request.method != "POST":
        return redirect(reverse("mybase:view_topic", args=[topic_slug]))

    if not request.user.is_authenticated:
        return redirect(reverse("mybase:view_topic", args=[topic_slug]))

    try:
        topic = Topic.objects.get(slug=topic_slug)
    except:
        return HttpResponse("Invalid topic")

    try:
        post = Page.objects.get(slug=post_slug, topic=topic)
    except:
        return HttpResponse("Invalid post")

    try:
        post_like = PostLike.objects.get(user=request.user, post=post, topic=topic)
        post_like.delete()
    except:
        post_like = PostLike(user=request.user, post=post, topic=topic)
        post_like.save()

    return redirect(reverse("mybase:view_topic", args=[topic.slug]))
