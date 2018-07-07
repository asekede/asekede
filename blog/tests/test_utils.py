from django.test import TestCase
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import datetime
from blog.models import Category, Post
from blog.utils import generate_archive, get_objects_by_page

import pytz


class UtilsTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Category')
        
        now = datetime(1994, 6, 19, 0, 0, 0, 0, tzinfo=pytz.UTC)
        Post.objects.create(title="Post 1", content="Post 1 Content", category=category, pub_date=now)
        Post.objects.create(title="Post 2", content="Post 2 Content", category=category, pub_date=now + timezone.timedelta(days=20))
        Post.objects.create(title="Post 3", content="Post 3 Content", category=category, pub_date=now - timezone.timedelta(days=20))
        Post.objects.create(title="Post 4", content="Post 4 Content", category=category, pub_date=now + timezone.timedelta(days=365))

    def tearDown(self):
        Post.objects.all().delete()
        Category.objects.all().delete()
    
    def test_get_objects_by_page(self):
        posts_list = Post.objects.all()
        if not Post._meta.ordering:
            posts_list = posts_list.order_by('-pub_date')
        paginator = Paginator(posts_list, 10)
        posts1, is_paginated1 = get_objects_by_page(paginator, 1)
        self.assertEqual(len(posts1), 4)
        self.assertEqual(posts1[0], posts_list[0])
        self.assertEqual(posts1[1], posts_list[1])
        self.assertEqual(posts1[2], posts_list[2])
        self.assertEqual(posts1[3], posts_list[3])
        self.assertEqual(is_paginated1, False)
        
        paginator = Paginator(posts_list, 2)
        posts2, is_paginated2 = get_objects_by_page(paginator, 1)
        self.assertEqual(len(posts2), 2)
        self.assertEqual(posts2[0], posts_list[0])
        self.assertEqual(posts2[1], posts_list[1])
        self.assertEqual(is_paginated2, True)
        posts3, is_paginated3 = get_objects_by_page(paginator, 2)
        self.assertEqual(len(posts3), 2)
        self.assertEqual(posts3[0], posts_list[2])
        self.assertEqual(posts3[1], posts_list[3])
        self.assertEqual(is_paginated3, True)

        posts4, is_paginated4 = get_objects_by_page(paginator, 3)
        self.assertEqual(len(posts4), 2)
        self.assertEqual(posts4[0], posts_list[2])
        self.assertEqual(posts4[1], posts_list[3])
        self.assertEqual(is_paginated4, True)

        posts5, is_paginated5 = get_objects_by_page(paginator, 'not an integer')
        self.assertEqual(len(posts5), 2)
        self.assertEqual(posts5[0], posts_list[0])
        self.assertEqual(posts5[1], posts_list[1])
        self.assertEqual(is_paginated5, True)

    def test_generate_archive(self):
        post1 = Post.objects.get(title="Post 1")
        post2 = Post.objects.get(title="Post 2")
        post3 = Post.objects.get(title="Post 3")
        post4 = Post.objects.get(title="Post 4")
        archive = generate_archive([post1, post2, post3, post4])
        test_archive = {
            "1995": {
                "number_of_posts": 1,
                "months": {
                    "June": {
                        "month_number": 6,
                        "number_of_posts": 1,
                        "posts": [post4]
                    }   
                }
            },
            "1994": {
                "number_of_posts": 3,
                "months": {
                    "July": {
                        "month_number": 7,
                        "number_of_posts": 1,
                        "posts": [post2]
                    },
                    "June": {
                        "month_number": 6,
                        "number_of_posts": 1,
                        "posts": [post1]
                    },
                    "May": {
                        "month_number": 5,
                        "number_of_posts": 1,
                        "posts": [post3]
                    }
                }
            }
        }
        self.assertDictEqual(archive, test_archive)
