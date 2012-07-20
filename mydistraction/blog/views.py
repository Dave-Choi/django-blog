from django.views.generic import ListView
from blog.models import Post
import datetime

#def posts_by_date(request, year, month, date):
def posts_by_date(request, *args, **kwargs):
    now = datetime.datetime.now()
    year = kwargs['year']
    month = kwargs['month']
    day = kwargs['day']

    list = Post.objects
    if(year):
        list = list.filter(date_published__year=year)
    if(month):
        list = list.filter(date_published__month=month)
    if(day):
        list = list.filter(date_published__day=day)

    list = list.order_by('-id')
    return ListView.as_view(
        queryset = list,
        context_object_name = 'post_list',
        template_name = 'blog/posts.html'
    )(request, *args, **kwargs)
