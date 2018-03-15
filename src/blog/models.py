from django.db import models
from django.http import Http404
from django.urls import reverse


class Tag(models.Model):
    class Meta:
        verbose_name='Tag'
        verbose_name_plural='Tags'

    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_list_of_tags():
        return Tag.objects.all()

    @staticmethod
    def get_tag_with_name(name):
        for tag in Tag.objects.all():
            if tag.get_name() == name:
                return tag
        raise Http404("Tag does not exist")
    
    def get_number_of_posts(self):
        return self.post_tags.count()

    def get_name(self):
        return ''.join([char if char.isalnum() else '_' for char in self.name])

    def get_url(self):
        return reverse('latest_posts_by_tag', args=[self.get_name()])


class Category(models.Model):
    class Meta:
        verbose_name='Category'
        verbose_name_plural='Categories'

    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_list_of_categories():
        return Category.objects.all()

    @staticmethod
    def get_category_with_name(name):
        for category in Category.objects.all():
            if category.get_name() == name:
                return category
        raise Http404("Category does not exist")
    
    def get_number_of_posts(self):
        return self.posts.filter(deleted=False).count() 

    def get_name(self):
        return ''.join([char if char.isalnum() else '_' for char in self.name])

    def get_url(self):
        return reverse('latest_posts_by_category', args=[self.get_name()])


class Post(models.Model):
    class Meta:
        verbose_name='Post'
        verbose_name_plural='Posts'

    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name="posts"
    )
    pub_date = models.DateTimeField()
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    @staticmethod
    def get_list_of_posts():
        posts = Post.objects.filter(deleted=False)
        return posts

    @staticmethod
    def get_list_of_latest_posts():
        posts = Post.get_list_of_posts().order_by('-pub_date')
        return posts

    @staticmethod
    def get_list_of_latest_posts_by_category(name):
        category = Category.get_category_with_name(name)
        posts = Post.get_list_of_latest_posts().filter(category=category)
        return posts

    @staticmethod
    def get_list_of_latest_posts_by_tag(name):
        tag = Tag.get_tag_with_name(name)
        posts = Post.get_list_of_latest_posts().annotate(
            exists=models.Exists(
                PostTag.objects.filter(
                    post=models.OuterRef('pk'),
                    tag=tag
                ) 
            )
        ).filter(exists=True)
        return posts

    @staticmethod
    def get_list_of_posts_by_year(year):
        posts = Post.get_list_of_latest_posts().filter(pub_date__year=year)
        return posts

    @staticmethod
    def get_list_of_posts_by_year_month(year, month):
        posts = Post.get_list_of_posts_by_year(year).filter(pub_date__month=month)
        return posts

    @staticmethod
    def get_list_of_posts_by_year_month_day(year, month, day):
        posts = Post.get_list_of_posts_by_year_month(year, month).filter(pub_date__day=day)
        return posts

    @staticmethod
    def get_post_by_year_month_day_title(year, month, day, title):
        for post in Post.get_list_of_posts_by_year_month_day(year, month, day):
            if post.get_title() == title:
                return post
        raise Http404("Post does not exist")

    def get_title(self):
        return ''.join([char if char.isalnum() else '_' for char in self.title])

    def get_url(self):
        time = self.pub_date
        return reverse('post_by_year_month_day_title', args=["%04d" % time.year, "%02d" % time.month, "%02d" % time.day, self.get_title()])
    
    #TODO need to add markdown
    def get_content(self):
        return self.content

    def get_abstract(self):
        content = self.get_content()
        pos = content.find(' ', 500)
        if pos != -1:
            return content[:pos] + '...'
        else:
            return content

    def get_tags(self):
        tags = Tag.get_list_of_tags().annotate(
            exists=models.Exists(
                PostTag.objects.filter(
                    post=self.pk,
                    tag=models.OuterRef('pk')
                )
            )
        ).filter(exists=True)
        return tags
    
    def has_next(self):
        return self.__get_next() != None

    def has_previous(self):
        return self.__get_previous() != None

    def __get_next(self):
        posts = Post.get_list_of_latest_posts().filter(
            pub_date__gt=self.pub_date
        )
        return posts[len(posts)-1] if len(posts) > 0 else None

    def get_next_url(self):
        return self.__get_next().get_url()

    def get_next_title(self):
        return self.__get_next().title

    def __get_previous(self):
        posts = Post.get_list_of_latest_posts().filter(
            pub_date__lt=self.pub_date
        )
        return posts[0] if len(posts) > 0 else None

    def get_previous_url(self):
        return self.__get_previous().get_url()

    def get_previous_title(self):
        return self.__get_previous().title


class PostTag(models.Model):
    class Meta:
        verbose_name='PostTag'
        verbose_name_plural='PostTags'
        unique_together=('post', 'tag')

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(
        Tag, 
        on_delete=models.CASCADE,
        related_name="post_tags"
    )

    def __str__(self):
        return "%d (Post: %s; Tag: %s)" % (self.id, self.post, self.tag)
