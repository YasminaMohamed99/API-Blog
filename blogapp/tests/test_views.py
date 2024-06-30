from django.contrib.auth.models import User
from django.test import TestCase
from blogapp.forms import *
from blogapp.models import *
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from blogapp.serializers import *


class ViewsTest(TestCase):

    def setUp(self):
        self.user, created = User.objects.get_or_create(username='testuser')
        if created:
            self.user.set_password('testpassword')
            self.user.save()
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.client.login(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.tag = Tag.objects.create(name='Test Tag')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.profile)
        self.post1 = Post.objects.create(title='Test Post1', content='Test Content1', author=self.profile)
        self.post.categories.add(self.category)
        self.post.tags.add(self.tag)
        self.comment = Comment.objects.create(content='Test Content', author=self.profile, post=self.post)
        self.comment1 = Comment.objects.create(content='Test Content1', author=self.profile, post=self.post)

    def test_sign_up_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UserForm)

        signup_data = {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'newuser@example.com',
            'first_name': 'test_firstname',
            'last_name': 'test_lastname',
        }
        response = self.client.post(reverse('register'), signup_data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_sign_in_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], LoginForm)
        User.objects.create_user(username='testuser2', password='testpassword')
        login_data = {'username': 'testuser2', 'password': 'testpassword'}
        response = self.client.post(reverse('login'), login_data)
        self.assertRedirects(response, reverse('all_posts'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_sign_out_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_list_posts_view(self):
        response = self.client.get(reverse('all_posts'))
        self.assertEqual(response.status_code, 200)

        self.assertIn('posts', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('tags', response.context)

        self.assertEqual(list(response.context['posts']), [self.post, self.post1])
        self.assertEqual(response.context['categories'][0], self.category)
        self.assertEqual(response.context['tags'][0], self.tag)

        self.assertTemplateUsed(response, 'all_posts.html')

    def test_create_post_view(self):
        self.client.force_login(self.user)
        url = reverse('create_post')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PostForm)
        self.assertTrue(response.context['create'])

        post_data = {
            'title': 'Test Post2',
            'content': 'Test Content2',
            'categories': [self.category.id],
            'tags': [self.tag.id],
        }
        response = self.client.post(url, post_data)
        self.assertRedirects(response, reverse('all_posts'))
        posts = Post.objects.filter(title='Test Post2', content='Test Content2', author=self.profile)
        self.assertEqual(posts.count(), 1)
        post = posts.first()
        self.assertEqual(list(post.categories.all()), [self.category])
        self.assertEqual(list(post.tags.all()), [self.tag])

    def test_update_post_view(self):
        self.client.force_login(self.user)
        url = reverse('update_post', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PostForm)
        self.assertFalse(response.context['create'])

        updated_data = {
            'title': 'Updated Title',
            'content': 'Updated Content',
            'categories': [],
            'tags': [],
        }
        response = self.client.post(url, updated_data)
        self.assertRedirects(response, reverse('all_posts'))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
        self.assertEqual(self.post.content, 'Updated Content')

    def test_del_post_view_post(self):
        self.client.force_login(self.user)

        url = reverse('delete_post', args=[self.post.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('all_posts'))
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=self.post.id)

    def test_show_comments_view(self):
        response = self.client.get(reverse('show_comments', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, 200)

        self.assertIn('comments', response.context)
        self.assertIn('post_id', response.context)

        expected_comments = [self.comment, self.comment1]
        actual_comments = list(response.context['comments'])
        self.assertEqual(actual_comments, expected_comments)

        self.assertEqual(response.context['post_id'], self.post.id)
        # self.assertEqual(list(response.context['comments']), [self.comment, self.comment1])

        self.assertTemplateUsed(response, 'comments.html')

    def test_add_comments_view(self):
        self.client.force_login(self.user)
        url = reverse('add_comments', args=[self.post.id])
        response = self.client.post(url, {'content': 'Test comment'})
        self.assertRedirects(response, reverse('show_comments', args=[self.post.id]))
        comments = Comment.objects.filter(post=self.post, content='Test comment')
        self.assertEqual(comments.count(), 1)
        self.assertEqual(comments.first().author, self.profile)

    def test_delete_comment_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_comment', args=[self.comment.id]))
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=self.comment.id)

        self.assertRedirects(response, reverse('show_comments', args=[self.post.id]))


class APITest(TestCase):

    def setUp(self):
        self.user, created = User.objects.get_or_create(username='testuser')
        if created:
            self.user.set_password('testpassword')
            self.user.save()
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.category = Category.objects.create(name='Test Category')
        self.tag = Tag.objects.create(name='Test Tag')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.profile)
        self.post.categories.add(self.category)
        self.post.tags.add(self.tag)
        self.comment = Comment.objects.create(content='Test Content', author=self.profile, post=self.post)

    def test_get_post(self):
        url = reverse('get-post', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post_serializer = PostSerializer(self.post)
        self.assertEqual(response.data, post_serializer.data)

    def test_update_post(self):
        url = reverse('get-post', args=[self.post.id])
        # updated_data = {'title': 'Updated Title', 'content': 'Updated Content', 'author': self.profile}
        updated_data = {
            "id": self.post.id,
            "title": "Updated Title",
            "content": "Updated Content",
            "created_at": self.post.created_at,
            "updated_at": self.post.updated_at,
            "author": self.profile.id,
            "categories": [cat.id for cat in self.post.categories.all()],
            "tags": [tag.id for tag in self.post.tags.all()]
        }
        response = self.client.post(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, updated_data['title'])
        self.assertEqual(self.post.content, updated_data['content'])

    def test_delete_post(self):
        url = reverse('get-post', args=[self.post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_categories(self):
        url = reverse('categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        categories = Category.objects.all()
        category_serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.data, category_serializer.data)

    def test_tags(self):
        url = reverse('tags')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tags = Tag.objects.all()
        tag_serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.data, tag_serializer.data)

    def test_comments_get(self):
        url = reverse('comments')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comments = Comment.objects.all()
        comment_serializer = CommentSerializer(comments, many=True)
        self.assertEqual(response.data, comment_serializer.data)

    def test_comments_post(self):
        url = reverse('comments')
        new_comment_data = {
            "id": self.comment.id,
            "content": "New Comment Content",
            "created_at": self.comment.created_at,
            "updated_at": self.comment.updated_at,
            "author": self.profile.id,
            "post": self.post.id
        }
        response = self.client.post(url, new_comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        created_comment = Comment.objects.last()
        self.assertEqual(created_comment.content, new_comment_data['content'])
        self.assertEqual(created_comment.post.id, new_comment_data['post'])

    def test_delete_comment(self):
        url = reverse('delete_comment', args=[self.comment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        # self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())
