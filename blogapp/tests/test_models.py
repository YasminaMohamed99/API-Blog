from django.contrib.auth.models import User
from django.test import TestCase

from blogapp.models import *


class ModelTest(TestCase):
    def setUp(self):
        self.user, created = User.objects.get_or_create(username='testuser')
        if created:
            self.user.set_password('testpassword')
            self.user.save()
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.profile.bio = 'Test bio'
        self.category = Category.objects.create(name='Test Category')
        self.tag = Tag.objects.create(name='Test Tag')
        self.post = Post.objects.create(title='Test Title', content='Test Content', author=self.profile)
        self.post.categories.add(self.category)
        self.post.tags.add(self.tag)
        self.comment = Comment.objects.create(content='Test Content', author=self.profile, post=self.post)

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.bio, 'Test bio')

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Test Category')
        self.assertIsNotNone(self.category.slug)

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, 'Test Tag')
        self.assertIsNotNone(self.tag.slug)

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Title')
        self.assertEqual(self.post.content, 'Test Content')
        self.assertEqual(self.post.author.user.username, 'testuser')
        self.assertTrue(self.post.categories.exists())
        self.assertTrue(self.post.tags.exists())

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, 'Test Content')
        self.assertEqual(self.comment.author.user.username, 'testuser')
        self.assertEqual(self.comment.post, self.post)