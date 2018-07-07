from django.test import TestCase
from django.urls import reverse


class UrlsTestCase(TestCase):
    def test_url_latest_posts(self):
        url = reverse('latest_posts', args=[])
        self.assertEqual(url, '/blog/')

    def test_url_posts_by_year(self):
        url = reverse('posts_by_year', args=[1994])
        self.assertEqual(url, '/blog/1994/')

    def test_url_posts_by_year_month(self):
        url = reverse('posts_by_year_month', args=[1994, 6])
        self.assertEqual(url, '/blog/1994/06/')

    def test_url_posts_by_year_month_day(self):
        url = reverse('posts_by_year_month_day', args=[1994, 6, 19])
        self.assertEqual(url, '/blog/1994/06/19/')

    def test_url_posts_by_year_month_day_title(self):
        url = reverse('post_by_year_month_day_title', args=[1994, 6, 19, 'Post_1'])
        self.assertEqual(url, '/blog/1994/06/19/Post_1/')

    def test_url_latest_posts_by_tag(self):
        url = reverse('latest_posts_by_tag', args=['Tag'])
        self.assertEqual(url, '/blog/tag/Tag/')

    def test_url_latest_posts_by_category(self):
        url = reverse('latest_posts_by_category', args=['Category'])
        self.assertEqual(url, '/blog/category/Category/')

