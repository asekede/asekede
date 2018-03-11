from django.test import TestCase
from django.http import Http404
from django.utils import timezone
from datetime import datetime
from .models import Tag, Category, Post, PostTag

import pytz


class TagTestCase(TestCase):
    def setUp(self):
        Tag.objects.create(name='Tag with whitespace')
        Tag.objects.create(name='TagWithoutWhitespace')
        Tag.objects.create(name='TagWithNumbers123456')
        Tag.objects.create(name='TagWithSymbols!@#$%^')

    def tearDown(self):
        Tag.objects.all().delete()
    
    def test_get_list_of_tags(self):
        tags = Tag.get_list_of_tags()
        self.assertEqual(len(tags), 4)
    
    def test_get_list_of_tags_when_no_tags(self):
        self.tearDown()
        tags = Tag.get_list_of_tags()
        self.assertEqual(list(tags), [])
    
    def test_get_tag_with_name(self):
        tag_with_whitespace = Tag.get_tag_with_name(name='Tag_with_whitespace')
        tag_without_whitespace = Tag.get_tag_with_name(name='TagWithoutWhitespace')
        tag_with_numbers = Tag.get_tag_with_name(name='TagWithNumbers123456')
        tag_with_symbols = Tag.get_tag_with_name(name='TagWithSymbols______')
        self.assertEqual(tag_with_whitespace.get_name(), 'Tag_with_whitespace')
        self.assertEqual(tag_without_whitespace.get_name(), 'TagWithoutWhitespace')
        self.assertEqual(tag_with_numbers.get_name(), 'TagWithNumbers123456')
        self.assertEqual(tag_with_symbols.get_name(), 'TagWithSymbols______')
    
    def test_get_tag_with_name_when_invalid(self):
        with self.assertRaises(Http404):
            Tag.get_tag_with_name('Tag with whitespace invalid') 
    

class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name='Category with whitespace')
        Category.objects.create(name='CategoryWithoutWhitespace')
        Category.objects.create(name='CategoryWithNumbers123456')
        Category.objects.create(name='CategoryWithSymbols!@#$%^')

    def tearDown(self):
        Category.objects.all().delete()

    def test_get_list_of_categories(self):
        categories = Category.get_list_of_categories()
        self.assertEqual(len(categories), 4)
    
    def test_get_list_of_categories_when_no_categories(self):
        self.tearDown()
        categories = Category.get_list_of_categories()
        self.assertEqual(list(categories), [])
    
    def test_get_category_with_name(self):
        category_with_whitespace = Category.get_category_with_name(name='Category_with_whitespace')
        category_without_whitespace = Category.get_category_with_name(name='CategoryWithoutWhitespace')
        category_with_numbers = Category.get_category_with_name(name='CategoryWithNumbers123456')
        category_with_symbols = Category.get_category_with_name(name='CategoryWithSymbols______')
        self.assertEqual(category_with_whitespace.get_name(), 'Category_with_whitespace')
        self.assertEqual(category_without_whitespace.get_name(), 'CategoryWithoutWhitespace')
        self.assertEqual(category_with_numbers.get_name(), 'CategoryWithNumbers123456')
        self.assertEqual(category_with_symbols.get_name(), 'CategoryWithSymbols______')
    
    def test_get_category_with_name_when_invalid(self):
        with self.assertRaises(Http404):
            Category.get_category_with_name('Category with whitespace invalid')


#TODO not finished
class PostTestCase(TestCase):
    def setUp(self):
        category_1 = Category.objects.create(name="Category 1")
        category_2 = Category.objects.create(name="Category 2")
        
        tag_1 = Tag.objects.create(name="Tag 1")
        tag_2 = Tag.objects.create(name="Tag 2")
        tag_3 = Tag.objects.create(name="Tag 3")
        tag_4 = Tag.objects.create(name="Tag 4")

        now = datetime(1994, 6, 19, 0, 0, 0, 0, tzinfo=pytz.UTC)
        post_1 = Post.objects.create(title="Post 1", content="Post 1 Content", category=category_1, pub_date=now)
        post_2 = Post.objects.create(title="Post 2", content="Post 2 Content", category=category_2, pub_date=now + timezone.timedelta(days=1))
        post_3 = Post.objects.create(title="Post 3", content="Post 3 Content", category=category_1, pub_date=now + timezone.timedelta(days=3))
        post_4 = Post.objects.create(title="Post 4", content="Post 4 Content", category=category_2, pub_date=now + timezone.timedelta(days=4))
        post_5 = Post.objects.create(title="Post 5", content="Post 5 Content", category=category_2, pub_date=now + timezone.timedelta(days=2))
        post_6 = Post.objects.create(title="Post 6", content="Post 6 Content", category=category_1, pub_date=now + timezone.timedelta(days=5))
        post_7 = Post.objects.create(title="Post 7", content="Post 7 Content", category=category_1, pub_date=now + timezone.timedelta(days=9))
        post_8 = Post.objects.create(title="Post 8", content="Post 8 Content", category=category_1, pub_date=now + timezone.timedelta(days=7))
        post_9 = Post.objects.create(title="Post 9", content="Post 9 Content", category=category_2, pub_date=now + timezone.timedelta(days=8))
        post_10 = Post.objects.create(title="Post 10", content="Post 10 Content", category=category_1, pub_date=now + timezone.timedelta(days=6))

        PostTag.objects.create(post=post_1, tag=tag_1)
        PostTag.objects.create(post=post_1, tag=tag_2)
        PostTag.objects.create(post=post_2, tag=tag_3)
        PostTag.objects.create(post=post_2, tag=tag_2)
        PostTag.objects.create(post=post_3, tag=tag_1)
        PostTag.objects.create(post=post_4, tag=tag_1)
        PostTag.objects.create(post=post_5, tag=tag_3)
        PostTag.objects.create(post=post_7, tag=tag_3)
        PostTag.objects.create(post=post_8, tag=tag_2)
        PostTag.objects.create(post=post_8, tag=tag_3)
        PostTag.objects.create(post=post_8, tag=tag_1)
        PostTag.objects.create(post=post_10, tag=tag_1)

    def tearDown(self):
        Post.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()
        PostTag.objects.all().delete()

    def test_get_list_of_latest_posts(self):
        posts = Post.get_list_of_latest_posts()
        self.assertEqual(len(posts), 10)
        self.assertEqual(posts[0].get_title(), "Post_7")
        self.assertEqual(posts[1].get_title(), "Post_9")
        self.assertEqual(posts[2].get_title(), "Post_8")
        self.assertEqual(posts[3].get_title(), "Post_10")
        self.assertEqual(posts[4].get_title(), "Post_6")
        self.assertEqual(posts[5].get_title(), "Post_4")
        self.assertEqual(posts[6].get_title(), "Post_3")
        self.assertEqual(posts[7].get_title(), "Post_5")
        self.assertEqual(posts[8].get_title(), "Post_2")
        self.assertEqual(posts[9].get_title(), "Post_1")

    def test_get_list_of_latest_posts_when_no_posts(self):
        self.tearDown()
        posts = Post.get_list_of_latest_posts()
        self.assertEqual(list(posts), [])

    def test_get_list_of_latest_posts_with_category(self):
        posts = Post.get_list_of_latest_posts_with_category('Category_1')
        self.assertEqual(len(posts), 6) 
        self.assertEqual(posts[0].get_title(), "Post_7")
        self.assertEqual(posts[1].get_title(), "Post_8")
        self.assertEqual(posts[2].get_title(), "Post_10")
        self.assertEqual(posts[3].get_title(), "Post_6")
        self.assertEqual(posts[4].get_title(), "Post_3")
        self.assertEqual(posts[5].get_title(), "Post_1")

    def test_get_list_of_latest_posts_with_category_when_invalid(self):
        with self.assertRaises(Http404):
            Post.get_list_of_latest_posts_with_category('Category Invalid')

    def test_get_list_of_latest_posts_with_tag(self):
        posts = Post.get_list_of_latest_posts_with_tag('Tag_1')
        self.assertEqual(len(posts), 5) 
        self.assertEqual(posts[0].get_title(), "Post_8")
        self.assertEqual(posts[1].get_title(), "Post_10")
        self.assertEqual(posts[2].get_title(), "Post_4")
        self.assertEqual(posts[3].get_title(), "Post_3")
        self.assertEqual(posts[4].get_title(), "Post_1")

    def test_get_list_of_latest_posts_with_tag_when_invalid(self):
        with self.assertRaises(Http404):
            Post.get_list_of_latest_posts_with_tag('Tag invalid')

    def test_get_list_of_latest_posts_with_tag_when_empty(self):
        posts = Post.get_list_of_latest_posts_with_tag('Tag_4')
        self.assertEqual(list(posts), [])

    def test_get_list_of_latest_posts_with_year(self):
        posts = Post.get_list_of_latest_posts_with_year(1994)
        self.assertEqual(len(posts), 10)
        self.assertEqual(posts[0].get_title(), "Post_7")
        self.assertEqual(posts[1].get_title(), "Post_9")
        self.assertEqual(posts[2].get_title(), "Post_8")
        self.assertEqual(posts[3].get_title(), "Post_10")
        self.assertEqual(posts[4].get_title(), "Post_6")
        self.assertEqual(posts[5].get_title(), "Post_4")
        self.assertEqual(posts[6].get_title(), "Post_3")
        self.assertEqual(posts[7].get_title(), "Post_5")
        self.assertEqual(posts[8].get_title(), "Post_2")
        self.assertEqual(posts[9].get_title(), "Post_1")
    
    def test_get_list_of_latest_posts_with_year_when_empty(self):
        posts = Post.get_list_of_latest_posts_with_year(1993)
        self.assertEqual(list(posts), [])

    def test_get_list_of_latest_posts_with_year_month(self):
        posts = Post.get_list_of_latest_posts_with_year_month(1994, 6)
        self.assertEqual(len(posts), 10)
        self.assertEqual(posts[0].get_title(), "Post_7")
        self.assertEqual(posts[1].get_title(), "Post_9")
        self.assertEqual(posts[2].get_title(), "Post_8")
        self.assertEqual(posts[3].get_title(), "Post_10")
        self.assertEqual(posts[4].get_title(), "Post_6")
        self.assertEqual(posts[5].get_title(), "Post_4")
        self.assertEqual(posts[6].get_title(), "Post_3")
        self.assertEqual(posts[7].get_title(), "Post_5")
        self.assertEqual(posts[8].get_title(), "Post_2")
        self.assertEqual(posts[9].get_title(), "Post_1")
    
    def test_get_list_of_latest_posts_with_year_month_when_empty(self):
        posts = Post.get_list_of_latest_posts_with_year_month(1994, 5)
        self.assertEqual(list(posts), [])

    def test_get_list_of_latest_posts_with_year_month_day(self):
        posts = Post.get_list_of_latest_posts_with_year_month_day(1994, 6, 24)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].get_title(), "Post_6")
    
    def test_get_list_of_latest_posts_with_year_month_day_when_empty(self):
        posts = Post.get_list_of_latest_posts_with_year_month_day(1994, 6, 18)
        self.assertEqual(list(posts), [])

    def test_get_post_with_year_month_day_title(self):
        post = Post.get_post_with_year_month_day_title(1994, 6, 24, 'Post_6')
        self.assertEqual(post.get_title(), "Post_6")
    
    def test_get_post_with_year_month_day_title_when_empty(self):
        with self.assertRaises(Http404):
            Post.get_post_with_year_month_day_title(1994, 6, 24, 'Post_1')
