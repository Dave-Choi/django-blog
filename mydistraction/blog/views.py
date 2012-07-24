from django.views.generic import ListView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from forms import PostForm
import datetime


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
        template_name = 'blog/posts/posts.html'
    )(request, *args, **kwargs)


def posts_by_author(request, *args, **kwargs):
    author = kwargs['author']

    list = Post.objects
    if(author):
        list = list.filter(author__name=author)
    return ListView.as_view(
        queryset = list,
        context_object_name = 'post_list',
        template_name = 'blog/posts/posts.html'
    )(request, *args, **kwargs)


@login_required
def post_write(request, *args, **kwargs):
    form = PostForm()
    return render(request, 'blog/posts/post_form.html', {
        'form': form,
    })
