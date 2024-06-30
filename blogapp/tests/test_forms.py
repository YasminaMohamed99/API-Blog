from django.test import TestCase, Client
from django.contrib.auth.models import User
from blogapp.forms import UserForm, LoginForm, ProfileForm, PostForm
from blogapp.models import Profile, Post, Category, Tag


class UserFormTest(TestCase):

    def test_user_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_form_invalid_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword123',
            'password2': 'differentpassword',
        }
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_user_form_invalid_email(self):
        form_data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class LoginFormTest(TestCase):

    def test_login_form_valid(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_missing_username(self):
        form_data = {
            'password': 'testpassword123',
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class ProfileFormTest(TestCase):
    def setUp(self):
        self.user, created = User.objects.get_or_create(username='testuser')
        if created:
            self.user.set_password('testpassword')
            self.user.save()
        self.profile, _ = Profile.objects.get_or_create(user=self.user)

    def test_profile_form_valid(self):
        form_data = {
            'bio': 'Updated bio content',
            'profile_picture': None,
            'email': 'test@example.com',
            'first_name': 'test first name',
            'last_name': 'test last name'
        }
        form = ProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_profile_form_missing_bio(self):
        form_data = {
            'bio': 'Updated bio content',
            'profile_picture': None,
            'email': 'test@example.com',
            'first_name': 'test first name',
            'last_name': 'test last name'
        }
        form = ProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())


class PostFormTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='TestCategory')
        self.tag = Tag.objects.create(name='TestTag')

    def test_post_form_valid(self):
        form_data = {
            'title': 'Test Title',
            'content': 'Test Content',
            'categories': [self.category.id],
            'tags': [self.tag.id],
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_form_missing_title(self):
        form_data = {
            'content': 'Test Content',
            'categories': [self.category.id],
            'tags': [self.tag.id],
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
