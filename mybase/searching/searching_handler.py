from .search_in_options import SearchIn
from .sort_by_options import SortBy

from mybase.models import Topic,Page

class SearchingHandler:
    def search(q, searchIn=SearchIn.ALL(), sortBy=SortBy.MOST_LIKED):
        # Adapted from: https://www.w3schools.com/django/django_queryset_filter.php
        topics = None
        posts = None
        if SearchIn.getVal(searchIn, SearchIn.TOPICS_IX) > 0:
            topics = Topic.objects.filter(name__icontains=q).values()
        if SearchIn.getVal(searchIn, SearchIn.POSTS_IX) > 0:
            posts = Page.objects.filter(title__icontains=q).values()
        return (posts, topics)
