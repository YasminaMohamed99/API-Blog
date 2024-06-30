from django.contrib.auth.models import User
from django.test import TestCase

from blogapp.models import Profile
from blogapp.serializers import *


class PostSerializerTest(TestCase):
    def setUp(self):
        self.user, created = User.objects.get_or_create(username='testuser')
        if created:
            self.user.set_password('testpassword')
            self.user.save()
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.client.login(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='TestCategory')
        self.tag = Tag.objects.create(name='TestTag')
        self.post_data = {
            'title': 'Test Title',
            'content': 'Test Content',
            'categories': [self.category.id],
            'tags': [self.tag.id],
            'author': self.profile.id
        }

    def test_post_serializer_valid(self):
        serializer = PostSerializer(data=self.post_data)
        self.assertTrue(serializer.is_valid())

    def test_post_serializer_invalid_missing_title(self):
        post_data = self.post_data.copy()
        post_data.pop('title')
        serializer = PostSerializer(data=post_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)


class CategorySerializerTest(TestCase):
    def test_category_serializer_valid(self):
        serializer = CategorySerializer(data={'name': 'TestCategory'})
        self.assertTrue(serializer.is_valid())

    def test_category_serializer_invalid_missing_name(self):
        serializer = CategorySerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)


class TagSerializerTest(TestCase):
    def test_tag_serializer_valid(self):
        serializer = TagSerializer(data={'name': 'TestTag'})
        self.assertTrue(serializer.is_valid())

    def test_tag_serializer_invalid_missing_name(self):
        serializer = TagSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)


class CommentSerializerTest(TestCase):
    def setUp(self):
        self.user, created = User.objects.get_or_create(username='testuser')
        if created:
            self.user.set_password('testpassword')
            self.user.save()
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.post = Post.objects.create(title='Test Title', content='Test Content', author=self.profile)
        self.comment_data = {
            'post': self.post.id,
            'content': 'Test Comment',
            'author': self.profile.id
        }

    def test_comment_serializer_valid(self):
        serializer = CommentSerializer(data=self.comment_data)
        self.assertTrue(serializer.is_valid())

    def test_comment_serializer_invalid_missing_content(self):
        comment_data = self.comment_data.copy()
        comment_data.pop('content')
        serializer = CommentSerializer(data=comment_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('content', serializer.errors)
