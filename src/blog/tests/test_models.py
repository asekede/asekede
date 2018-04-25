from django.test import TestCase
from django.http import Http404
from django.utils import timezone
from datetime import datetime
from blog.models import Tag, Category, Post, PostTag

import pytz

class TagTestCase(TestCase):
    def setUp(self):
        Tag.objects.create(name='Tag 1')
        Tag.objects.create(name='Tag_2')
        Tag.objects.create(name='Tag3')
        Tag.objects.create(name='Tag#4')

    def tearDown(self):
        Tag.objects.all().delete()
    
    def test_to_str(self):  
        tag1 = Tag.objects.get(name='Tag 1')
        tag2 = Tag.objects.get(name='Tag_2')
        tag3 = Tag.objects.get(name='Tag3')
        tag4 = Tag.objects.get(name='Tag#4')
        self.assertEqual(str(tag1), 'Tag 1')
        self.assertEqual(str(tag2), 'Tag_2')
        self.assertEqual(str(tag3), 'Tag3')
        self.assertEqual(str(tag4), 'Tag#4')

    def test_get_list_of_tags(self):
        tags = Tag.get_list_of_tags()
        self.assertEqual(len(tags), 4)
    
    def test_get_list_of_tags_when_no_tags(self):
        self.tearDown()
        tags = Tag.get_list_of_tags()
        self.assertEqual(list(tags), [])
    
    def test_get_tag_with_name(self):
        tag1 = Tag.get_tag_with_name(name='Tag_1')
        tag2 = Tag.get_tag_with_name(name='Tag_2')
        tag3 = Tag.get_tag_with_name(name='Tag3')
        tag4 = Tag.get_tag_with_name(name='Tag_4')
        self.assertEqual(tag1.name, 'Tag 1')
        self.assertEqual(tag2.name, 'Tag_2')
        self.assertEqual(tag3.name, 'Tag3')
        self.assertEqual(tag4.name, 'Tag#4')
    
    def test_get_tag_with_name_when_invalid(self):
        with self.assertRaises(Http404):
            Tag.get_tag_with_name('Tag invalid') 
    

class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name='Category 1')
        Category.objects.create(name='Category_2')
        Category.objects.create(name='Category3')
        Category.objects.create(name='Category#4')

    def tearDown(self):
        Category.objects.all().delete()
    
    def test_to_str(self):
        category1 = Category.objects.get(name='Category 1')
        category2 = Category.objects.get(name='Category_2')
        category3 = Category.objects.get(name='Category3')
        category4 = Category.objects.get(name='Category#4')
        self.assertEqual(str(category1), 'Category 1')
        self.assertEqual(str(category2), 'Category_2')
        self.assertEqual(str(category3), 'Category3')
        self.assertEqual(str(category4), 'Category#4')

    def test_get_list_of_categories(self):
        categories = Category.get_list_of_categories()
        self.assertEqual(len(categories), 4)
    
    def test_get_list_of_categories_when_no_categories(self):
        self.tearDown()
        categories = Category.get_list_of_categories()
        self.assertEqual(list(categories), [])
    
    def test_get_category_with_name(self):
        category1 = Category.get_category_with_name(name='Category_1')
        category2 = Category.get_category_with_name(name='Category_2')
        category3 = Category.get_category_with_name(name='Category3')
        category4 = Category.get_category_with_name(name='Category_4')
        self.assertEqual(category1.name, 'Category 1')
        self.assertEqual(category2.name, 'Category_2')
        self.assertEqual(category3.name, 'Category3')
        self.assertEqual(category4.name, 'Category#4')
    
    def test_get_category_with_name_when_invalid(self):
        with self.assertRaises(Http404):
            Category.get_category_with_name('Category with whitespace invalid')


class PostTestCase(TestCase):
    def setUp(self):
        category_1 = Category.objects.create(name="Category 1")
        category_2 = Category.objects.create(name="Category 2")
        category_3 = Category.objects.create(name="Category 3")
        
        tag_1 = Tag.objects.create(name="Tag 1")
        tag_2 = Tag.objects.create(name="Tag 2")
        tag_3 = Tag.objects.create(name="Tag 3")
        tag_4 = Tag.objects.create(name="Tag 4")

        now = datetime(1994, 6, 19, 0, 0, 0, 0, tzinfo=pytz.UTC)
        post_1 = Post.objects.create(title="Post 1", content="Post 1 Content", category=category_1, pub_date=now)
        post_2 = Post.objects.create(title="Post 2", content="{} Post 2 Content".format("."*500), category=category_2, pub_date=now + timezone.timedelta(days=1))
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
    
    def test_to_string(self):
        post = Post.objects.get(title='Post 1')
        self.assertEqual(str(post), 'Post 1')

    def test_get_list_of_posts(self):
        posts = Post.get_list_of_posts()
        self.assertEqual(len(posts), 10)
        self.assertEqual(posts[0].get_title(), "Post_1")
        self.assertEqual(posts[1].get_title(), "Post_2")
        self.assertEqual(posts[2].get_title(), "Post_3")
        self.assertEqual(posts[3].get_title(), "Post_4")
        self.assertEqual(posts[4].get_title(), "Post_5")
        self.assertEqual(posts[5].get_title(), "Post_6")
        self.assertEqual(posts[6].get_title(), "Post_7")
        self.assertEqual(posts[7].get_title(), "Post_8")
        self.assertEqual(posts[8].get_title(), "Post_9")
        self.assertEqual(posts[9].get_title(), "Post_10")

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

    def test_get_list_of_latest_posts_by_category(self):
        posts = Post.get_list_of_latest_posts_by_category('Category_1')
        self.assertEqual(len(posts), 6) 
        self.assertEqual(posts[0].get_title(), "Post_7")
        self.assertEqual(posts[1].get_title(), "Post_8")
        self.assertEqual(posts[2].get_title(), "Post_10")
        self.assertEqual(posts[3].get_title(), "Post_6")
        self.assertEqual(posts[4].get_title(), "Post_3")
        self.assertEqual(posts[5].get_title(), "Post_1")

    def test_get_list_of_latest_posts_by_category_when_invalid(self):
        with self.assertRaises(Http404):
            Post.get_list_of_latest_posts_by_category('Category Invalid')
    
    def test_get_list_of_latest_posts_by_category_when_empty(self):
        with self.assertRaises(Http404):
            Post.get_list_of_latest_posts_by_category('Category_3')

    def test_get_list_of_latest_posts_by_tag(self):
        posts = Post.get_list_of_latest_posts_by_tag('Tag_1')
        self.assertEqual(len(posts), 5) 
        self.assertEqual(posts[0].get_title(), "Post_8")
        self.assertEqual(posts[1].get_title(), "Post_10")
        self.assertEqual(posts[2].get_title(), "Post_4")
        self.assertEqual(posts[3].get_title(), "Post_3")
        self.assertEqual(posts[4].get_title(), "Post_1")

    def test_get_list_of_latest_posts_by_tag_when_invalid(self):
        with self.assertRaises(Http404):
            Post.get_list_of_latest_posts_by_tag('Tag invalid')

    def test_get_list_of_latest_posts_by_tag_when_empty(self):
        with self.assertRaises(Http404):
            Post.get_list_of_latest_posts_by_tag('Tag_4')

    def test_get_list_of_posts_by_year(self):
        posts = Post.get_list_of_posts_by_year(1994)
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
    
    def test_get_list_of_posts_by_year_when_empty(self):
        with self.assertRaises(Http404):
            Post.get_list_of_posts_by_year(1993)

    def test_get_list_of_posts_by_year_month(self):
        posts = Post.get_list_of_posts_by_year_month(1994, 6)
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
    
    def test_get_list_of_posts_by_year_month_when_empty(self):
        with self.assertRaises(Http404):
            Post.get_list_of_posts_by_year_month(1994, 5)

    def test_get_list_of_posts_by_year_month_day(self):
        posts = Post.get_list_of_posts_by_year_month_day(1994, 6, 24)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].get_title(), "Post_6")
    
    def test_get_list_of_posts_by_year_month_day_when_empty(self):
        with self.assertRaises(Http404):
            Post.get_list_of_posts_by_year_month_day(1994, 6, 18)

    def test_get_post_by_year_month_day_title(self):
        post = Post.get_post_by_year_month_day_title(1994, 6, 24, 'Post_6')
        self.assertEqual(post.get_title(), "Post_6")
    
    def test_get_post_by_year_month_day_title_when_empty(self):
        with self.assertRaises(Http404):
            Post.get_post_by_year_month_day_title(1994, 6, 24, 'Post_1')

    def test_get_url(self):
        post = Post.objects.get(title="Post 1")
        self.assertEqual(post.get_url(), "/blog/1994/06/19/Post_1/")
    
    def test_get_abstract(self):
        post = Post.objects.get(title="Post 1")
        self.assertEqual(post.get_abstract(), "Post 1 Content")
    
    def test_get_abstract_when_content_is_long(self):
        post = Post.objects.get(title="Post 2")
        self.assertEqual(post.get_abstract(), "{}...".format("."*500))

class PostTagTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Category")
        tag = Tag.objects.create(name="Tag")
        now = datetime(1994, 6, 19, 0, 0, 0, 0, tzinfo=pytz.UTC)
        post = Post.objects.create(title="Post", content="Post Content", category=category, pub_date=now)
        PostTag.objects.create(post=post, tag=tag)

    def tearDown(self):
        Post.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()
        PostTag.objects.all().delete()

    def test_to_string(self):
        post = Post.objects.get(title="Post")
        tag = Tag.objects.get(name="Tag")
        post_tag = PostTag.objects.get(post=post, tag=tag)
        self.assertEqual(str(post_tag), '1 (Post: Post; Tag: Tag)')
