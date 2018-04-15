from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse
from django.views import View
from django.core.paginator import Paginator
from django.template import RequestContext
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from .models import Tag, Category, Post, PostTag
from .utils import get_objects_by_page, generate_archive


class PostsView(View):
    template_name = 'blog.html'

    def get_posts_list(self, *args, **kwargs):
        return Post.get_list_of_posts()
    
    def get_categories_list(self, *args, **kwargs):
        return Category.get_list_of_categories()
    
    def get_tags_list(self, *args, **kwargs):
        return Tag.get_list_of_tags()
    
    def get_posts_archive(self, *args, **kwargs):
        posts = Post.get_list_of_latest_posts()
        return generate_archive(posts)

    def get_title(self, *args, **kwargs):
        return 'Posts'

    def get(self, request, *args, **kwargs):
        posts_list = self.get_posts_list(*args, **kwargs)
        paginator = Paginator(posts_list, 10)
        posts, is_paginated = get_objects_by_page(paginator, request.GET.get('page'))
        archive = self.get_posts_archive(*args, **kwargs)
        categories = self.get_categories_list(*args, **kwargs)
        tags = self.get_tags_list(*args, **kwargs)
        context = {
            'title': self.get_title(*args, **kwargs),
            'is_paginated': is_paginated,
            'posts': posts,
            'archive': archive,
            'categories': categories,
            'tags': tags
        }
        return render(request, self.template_name, context)

class LatestPostsView(PostsView):
    def get_posts_list(self, *args, **kwargs):
        return Post.get_list_of_latest_posts()
    
    def get_title(self, *args, **kwargs):
        return 'Blog -> latest posts'


class PostsByYearView(PostsView):
    def get_posts_list(self, *args, **kwargs):
        return Post.get_list_of_posts_by_year(year=kwargs.get('year'))
    
    def get_title(self, *args, **kwargs):
        return 'Blog -> posts in {}'.format(kwargs.get('year'))


class PostsByYearMonthView(PostsView):
    def get_posts_list(self, *args, **kwargs):
        return Post.get_list_of_posts_by_year_month(
            year=kwargs.get('year'),
            month=kwargs.get('month')
        )
    
    def get_title(self, *args, **kwargs):
        return 'Blog -> posts in {}.{}'.format(
            kwargs.get('month'),
            kwargs.get('year')
        )


class PostsByYearMonthDayView(PostsView):
    def get_posts_list(self, *args, **kwargs):
        return Post.get_list_of_posts_by_year_month_day(
            year=kwargs.get('year'),
            month=kwargs.get('month'),
            day=kwargs.get('day')
        )
    
    def get_title(self, *args, **kwargs):
        return 'Blog -> posts in {}.{}.{}'.format(
            kwargs.get('day'),
            kwargs.get('month'),
            kwargs.get('year')
        )

class PostsByTagView(PostsView):
    def get_posts_list(self, *args, **kwargs):
        return Post.get_list_of_latest_posts_by_tag(
            name=kwargs.get('name'),
        )
    
    def get_title(self, *args, **kwargs):
        return 'Blog -> posts by tag: {}'.format(
            kwargs.get('name')        
        )


class PostsByCategoryView(PostsView):
    def get_posts_list(self, *args, **kwargs):
        return Post.get_list_of_latest_posts_by_category(
            name=kwargs.get('name'),
        )
    
    def get_title(self, *args, **kwargs):
        return 'Blog -> posts by category: {}'.format(
            kwargs.get('name')        
        )


class PostByYearMonthDayTitleView(View):
    template_name = 'post.html'

    def get_post(self, *args, **kwargs):
        return Post.get_post_by_year_month_day_title(
            year=kwargs.get('year'),
            month=kwargs.get('month'),
            day=kwargs.get('day'),
            title=kwargs.get('title')
        )

    def get_posts_archive(self, *args, **kwargs):
        posts = Post.get_list_of_latest_posts()
        return generate_archive(posts)

    def get_categories_list(self, *args, **kwargs):
        return Category.get_list_of_categories()
    
    def get_tags_list(self, *args, **kwargs):
        return Tag.get_list_of_tags()
 
    def get(self, request, *args, **kwargs):
        post = self.get_post(*args, **kwargs)
        archive = self.get_posts_archive(*args, **kwargs)
        categories = self.get_categories_list(*args, **kwargs)
        tags = self.get_tags_list(*args, **kwargs)
        context = {
            'title': post.title,
            'post': post,
            'archive': archive,
            'categories': categories,
            'tags': tags
        }
        return render(request, self.template_name, context)

class LatestPostsFeed(Feed):
    title = "Personal blog of Assylkhan Abdrakhmanov"
    link = '/feed/'
    description = "I am a back-end developer."

    def items(self):
        return Post.get_list_of_latest_posts(number=10)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.get_abstract()

    def item_link(self, item):
        return item.get_url()

class LatestPostsFeedAtom(LatestPostsFeed):
    feed_type = Atom1Feed
    subtitle = LatestPostsFeed.description

def handler404(request, exception):
    response = render_to_response(
        '404.html', 
        {}, 
        context_instance=RequestContext(request)
    )
    response.status_code = 404
    return response

def handler500(request, exception):
    response = render_to_response(
        '500.html', 
        {}, 
        context_instance=RequestContext(request)
    )
    response.status_code = 500
    return response
