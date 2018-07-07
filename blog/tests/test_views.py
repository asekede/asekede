from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from datetime import datetime
from blog.models import Tag, Category, Post, PostTag

import pytz


class ViewsTestCase(TestCase):
    def setUp(self):
        category_1 = Category.objects.create(name='Category 1')
        category_2 = Category.objects.create(name='Category 2')

        tag_1 = Tag.objects.create(name='Tag 1')
        tag_2 = Tag.objects.create(name='Tag 2')
    
        now = datetime(1994, 6, 19, 0, 0, 0, 0, tzinfo=pytz.UTC)
        post_1 = Post.objects.create(title='Post 1', content='Post 1 Content', category=category_1, pub_date=now)
        post_2 = Post.objects.create(title='Post 2', content='Post 2 Content', category=category_1, pub_date=now + timezone.timedelta(days=30))
        post_3 = Post.objects.create(title='Post 3', content='Post 3 Content', category=category_2, pub_date=now + timezone.timedelta(days=365))
        post_4 = Post.objects.create(title='Post 4', content='Post 4 Content', category=category_2, pub_date=now - timezone.timedelta(days=365))
        
        PostTag.objects.create(post=post_1, tag=tag_1)
        PostTag.objects.create(post=post_1, tag=tag_2)
        PostTag.objects.create(post=post_2, tag=tag_1)
        PostTag.objects.create(post=post_3, tag=tag_2)

    def tearDown(self):
        Post.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()
        PostTag.objects.all().delete()
    
    def test_latest_posts(self):
        response = self.client.get(reverse('latest_posts', args=[]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog.html')

    def test_posts_by_year(self):
        response = self.client.get(reverse('posts_by_year', args=[1994]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog.html')

    def test_posts_by_year_month(self):
        response = self.client.get(reverse('posts_by_year_month', args=[1994, 6]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog.html')
    
    def test_posts_by_year_month_day(self):
        response = self.client.get(reverse('posts_by_year_month_day', args=[1994, 6, 19]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog.html')

    def test_posts_by_tag(self):
        response = self.client.get(reverse('latest_posts_by_tag', args=['Tag_1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog.html')

        response = self.client.get(reverse('latest_posts_by_tag', args=['Wrong_Tag']))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_posts_by_category(self):
        response = self.client.get(reverse('latest_posts_by_category', args=['Category_1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog.html')

        response = self.client.get(reverse('latest_posts_by_category', args=['Wrong_Category']))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_post_by_year_month_day_title(self):
        post = Post.objects.get(title='Post 1')
        response = self.client.get(post.get_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post.html')
        self.assertContains(response, post.title)

        response = self.client.get(reverse('post_by_year_month_day_title', args=[2018, 1, 1, 'Some_title']))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_latest_posts_feed(self):
        response = self.client.get(reverse('feed', args=[]))
        self.assertEqual(response.status_code, 200)

    def test_latest_posts_feed_atom(self):
        response = self.client.get(reverse('feed_atom', args=[]))
        self.assertEqual(response.status_code, 200)
