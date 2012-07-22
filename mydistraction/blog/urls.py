from django.conf.urls import patterns, include, url
from models import author_name_pattern, author_slug_pattern
from django.views.generic import DetailView, ListView
from blog.models import Post, Author
import re
from blog.views import posts_by_date, posts_by_author


# Post Patterns
urlpatterns = patterns('',
    # all posts
    url(
        r'^posts/$',
        ListView.as_view(
            queryset = Post.objects.order_by('-id')[:10],
            context_object_name = 'post_list',
            template_name = 'blog/posts/posts.html'
        )
    ),

    # posts by id
    url(
        r'^posts/($P<pk>\d+)/$',
        DetailView.as_view(
            model = Post,
            template_name = 'blog/posts/post_single.html'
        )
    ),

    # posts by year [, month [and day]]
    url(
        r'^posts/date/(?P<year>\d{4})/((?P<month>\d{1,2})/((?P<day>\d{1,2})/)?)?$',
        posts_by_date
    ),

    # posts by author
    url(
        r'^posts/author/(?P<s>%s)/$' % author_slug_pattern,
        posts_by_author
    )
)


# Author Patterns
urlpatterns += patterns('',
    # all authors
    url(
        r'^authors/$',
        ListView.as_view(
            queryset = Author.objects.all(),
            context_object_name = 'author_list',
            template_name = 'blog/authors/authors.html'
        )
    ),

    # author by id
    url(
        r'^authors/(?P<slug>%s)/$' % author_slug_pattern,
        DetailView.as_view(
            model = Author,
            slug_field = 'display_name',
            template_name = 'blog/authors/author_single.html'
        )
    )
)
