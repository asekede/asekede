from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views import View
from django.core.paginator import Paginator

from .models import Tag, Category, Post, PostTag
from .utils import get_objects_by_page


class LatestPostsView(View):
    template_name = 'blog.html'

    def get(self, request, *args, **kwargs):
        posts_list = Post.get_list_of_latest_posts()
        paginator = Paginator(posts_list, 10)
        
        posts = get_objects_by_page(
            paginator,
            request.GET.get('page')
        )
        
        categories = Category.get_list_of_categories()
        tags = Tag.get_list_of_tags()

        context = {
            'title': 'Latest posts',
            'posts': posts,
            'categories': categories,
            'tags': tags
        }
        return render(request, self.template_name, context)


class PostsByYearView(View):
    template_name = 'blog.html'

    def get(self, request, *args, **kwargs):
        posts_list = Post.get_list_of_posts_by_year(
            kwargs.get('year')
        )
        paginator = Paginator(posts_list, 10)
        
        posts = get_objects_by_page(
            paginator,
            request.GET.get('page')
        )

        categories = Category.get_list_of_categories()
        tags = Tag.get_list_of_tags()
        
        context = {
            'title': 'Posts by {}'.format(
                kwargs.get('year')
            ),
            'posts': posts,
            'categories': categories,
            'tags': tags
        }
        return render(request, self.template_name, context)


class PostsByYearMonthView(View):
    template_name = 'blog.html'

    def get(self, request, *args, **kwargs):
        posts_list = Post.get_list_of_posts_by_year_month(
            kwargs.get('year'), 
            kwargs.get('month')
        )
        paginator = Paginator(posts_list, 10)
        
        posts = get_objects_by_page(
            paginator,
            request.GET.get('page')
        )

        context = {
            'title': 'Posts by {} {}'.format(
                kwargs.get('year'),
                kwargs.get('month')
            ),
            'posts': posts
        }
        return render(request, self.template_name, context)


class PostsByYearMonthDayView(View):
    template_name = 'blog.html'

    def get(self, request, *args, **kwargs):
        posts_list = Post.get_list_of_posts_by_year_month_day(
            kwargs.get('year'), 
            kwargs.get('month'),
            kwargs.get('day')
        )
        paginator = Paginator(posts_list, 10)
        
        posts = get_objects_by_page(
            paginator,
            request.GET.get('page')
        )

        context = {
            'title': 'Posts by {} {} {}'.format(
                kwargs.get('year'),
                kwargs.get('month'),
                kwargs.get('day')
            ),
            'posts': posts
        }
        return render(request, self.template_name, context)


class PostByYearMonthDayTitleView(View):
    template_name = 'post.html'

    def get(self, request, *args, **kwargs):
        post = Post.get_post_by_year_month_day_title(
            kwargs.get('year'), 
            kwargs.get('month'),
            kwargs.get('day'),
            kwargs.get('title')
        )

        context = {
            'title': kwargs.get('title'),
            'post': post
        }
        return render(request, self.template_name, context)


class PostsByTagView(View):
    template_name = 'blog.html'

    def get(self, request, *args, **kwargs):
        posts_list = Post.get_list_of_latest_posts_by_tag(
            kwargs.get('name')
        )
        paginator = Paginator(posts_list, 10)
        
        posts = get_objects_by_page(
            paginator,
            request.GET.get('page')
        )

        context = {
            'title': 'Posts by {}'.format(
                kwargs.get('name')
            ),
            'posts': posts
        }
        return render(request, self.template_name, context)


class PostsByCategoryView(View):
    template_name = 'blog.html'

    def get(self, request, *args, **kwargs):
        posts_list = Post.get_list_of_latest_posts_by_category(
            kwargs.get('name')
        )
        paginator = Paginator(posts_list, 10)
        
        posts = get_objects_by_page(
            paginator,
            request.GET.get('page')
        )

        context = {
            'title': 'Posts by {}'.format(
                kwargs.get('name')
            ),
            'posts': posts
        }
        return render(request, self.template_name, context)
