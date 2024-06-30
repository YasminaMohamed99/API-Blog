from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve

from blogapp.models import Profile
from blogapp.views import *


class UrlsTest(SimpleTestCase):

    def test_sign_in_url_is_resolved(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, sign_in)

    def test_list_posts_url_is_resolved(self):
        url = reverse('all_posts')
        self.assertEqual(resolve(url).func, list_posts)

    def test_sign_up_url_is_resolved(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, sign_up)

    def test_manage_profile_url_is_resolved(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func, manage_profile)

    def test_edit_profile_url_is_resolved(self):
        url = reverse('edit_profile')
        self.assertEqual(resolve(url).func, edit_profile)

    def test_show_comments_url_is_resolved(self):
        url = reverse('show_comments', kwargs={'post_id': 1})
        self.assertEqual(resolve(url).func, show_comments)

    def test_add_comments_url_is_resolved(self):
        url = reverse('add_comments', kwargs={'post_id': 1})
        self.assertEqual(resolve(url).func, add_comments)

    def test_delete_comment_url_is_resolved(self):
        url = reverse('delete_comment', kwargs={'comment_id': 1})
        self.assertEqual(resolve(url).func, del_comment)

    def test_create_post_url_is_resolved(self):
        url = reverse('create_post')
        self.assertEqual(resolve(url).func, create_post)

    def test_update_post_url_is_resolved(self):
        url = reverse('update_post', kwargs={'post_id': 1})
        self.assertEqual(resolve(url).func, update_post)

    def test_delete_post_url_is_resolved(self):
        url = reverse('delete_post', kwargs={'post_id': 1})
        self.assertEqual(resolve(url).func, del_post)

    def test_search_posts_url_is_resolved(self):
        url = reverse('search_posts')
        self.assertEqual(resolve(url).func, search)

    def test_sign_out_url_is_resolved(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, sign_out)

    def test_api_posts_url_is_resolved(self):
        url = reverse('posts')
        self.assertEqual(resolve(url).func, posts)

    def test_api_get_post_url_is_resolved(self):
        url = reverse('get-post', kwargs={"post_id": 1})
        self.assertEqual(resolve(url).func, get_post)

    def test_api_categories_url_is_resolved(self):
        url = reverse('categories')
        self.assertEqual(resolve(url).func, categories)

    def test_api_tags_url_is_resolved(self):
        url = reverse('tags')
        self.assertEqual(resolve(url).func, tags)

    def test_api_comments_url_is_resolved(self):
        url = reverse('comments')
        self.assertEqual(resolve(url).func, comments)

    def test_api_delete_comment_url_is_resolved(self):
        url = reverse('delete-comment', kwargs={"comment_id": 1})
        self.assertEqual(resolve(url).func, delete_comment)


class UrlsResponseTest(TestCase):

    def setUp(self):
        self.user, created = User.objects.get_or_create(username='testuser')
        if created:
            self.user.set_password('testpassword')
            self.user.save()
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.category = Category.objects.create(name='Test Category')
        self.tag = Tag.objects.create(name='Test Tag')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.profile
        )
        self.post.categories.add(self.category)
        self.post.tags.add(self.tag)
        self.client.login(username='testuser', password='testpassword')

    def test_sign_in_url_response(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_list_posts_url_response(self):
        response = self.client.get(reverse('all_posts'))
        self.assertEqual(response.status_code, 200)

    def test_sign_up_url_response(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_manage_profile_url_response(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_url_response(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)

    def test_show_comments_url_response(self):
        response = self.client.get(reverse('show_comments', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, 200)

    def test_add_comments_url_response(self):
        response = self.client.get(reverse('add_comments', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, 200)

    def test_delete_comment_url_response(self):
        comment = Comment.objects.create(post=self.post, author=self.profile, content='Test Comment')
        response = self.client.get(reverse('delete_comment', kwargs={'comment_id': comment.id}))
        self.assertEqual(response.status_code, 302)  # return 302 when the function redirect after successfully deleting

    def test_create_post_url_response(self):
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 200)

    def test_update_post_url_response(self):
        response = self.client.get(reverse('update_post', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, 200)

    def test_delete_post_url_response(self):
        response = self.client.get(reverse('delete_post', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, 302)

    def test_search_posts_url_response(self):
        response = self.client.get(reverse('search_posts'))
        self.assertEqual(response.status_code, 200)

    def test_sign_out_url_response(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_api_posts_url_response(self):
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, 200)

    def test_api_get_post_url_response(self):
        response = self.client.get(reverse('get-post', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, 200)

    def test_api_categories_url_response(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)

    def test_api_tags_url_response(self):
        response = self.client.get(reverse('tags'))
        self.assertEqual(response.status_code, 200)

    def test_api_comments_url_response(self):
        response = self.client.get(reverse('comments'))
        self.assertEqual(response.status_code, 200)

    def test_api_delete_comment_url_response(self):
        comment = Comment.objects.create(post=self.post, author=self.profile, content='Test Comment')
        response = self.client.get(reverse('delete_comment', kwargs={"comment_id": comment.id}))
        self.assertEqual(response.status_code, 302)
