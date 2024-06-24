from django.contrib import admin

from blogapp.models import Profile, Category, Tag, Post, Comment

# Register your models here.
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)

