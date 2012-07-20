from django.conf.urls import patterns, include, url
from models import author_name_pattern
from django.views.generic import DetailView, ListView
from blog.models import Post, Author
import re
from blog.views import posts_by_date

urlpatterns = patterns('',
    #all posts
    url(
        r'^posts/$',
        ListView.as_view(
            queryset = Post.objects.order_by('-id')[:10],
            context_object_name = 'post_list',
            template_name = 'blog/posts.html'
        )
    ),

    url(
        r'^posts/($P<pk>\d+)/$',
        DetailView.as_view(
            model = Post,
            template_name = 'blog/post_single.html'
        )
    ),

    #posts by year, month and day
    url(
        r'^posts/date/(?P<year>\d{4})/((?P<month>\d{1,2})/((?P<day>\d{1,2})/)?)?$', posts_by_date
    ),

    #posts by author
    url(
        re.compile('^author/(%s)/$' % author_name_pattern),
        #r'^author/(.+)/$',
        ListView.as_view(
            queryset = Post.objects.order_by('-id')[:10],
            context_object_name = 'latest_post_list',
            template_name = 'blog/index.html'
        )
    )
)
