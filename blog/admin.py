from django.contrib import admin

from .models import Tag, Category, Post, PostTag

admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostTag)
