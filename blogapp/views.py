from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

from blogapp.forms import UserForm, LoginForm, ProfileForm, PostForm
from blogapp.models import Post, Category, Tag, Comment
from blogapp.serializers import PostSerializer, CategorySerializer, TagSerializer, CommentSerializer


def search(request):
    query = request.GET.get('q')
    results = None
    if query:
        results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    return render(request, 'all_posts.html',
                  {'query': query, 'posts': results, "categories": Category.objects.all(), "tags": Tag.objects.all()})


def sign_up(request):
    if request.method == 'POST':
        signup_form = UserForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            messages.info(request, "User account created successfully")
            return redirect('login')
    else:
        signup_form = UserForm()
    return render(request, 'signup.html', {'form': signup_form})


def sign_in(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if request.GET.get('next') is not None:
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('all_posts')
            else:
                messages.info(request, "User name or password isn't incorrect")
    else:
        login_form = LoginForm()
    return render(request, 'login.html', {'form': login_form})


def sign_out(request):
    logout(request)
    return redirect('login')


def list_posts(request):
    all_posts = Post.objects.all()
    return render(request, "all_posts.html",
                  {"posts": all_posts, "categories": Category.objects.all(), "tags": Tag.objects.all()})


def apply_filter(request):
    category = request.GET.get('category') or ''
    tag = request.GET.get('tag') or ''
    if category:
        all_posts = Post.objects.filter(categories=category)
    if tag:
        all_posts = Post.objects.filter(tags=tag)
    return render(request, "all_posts.html",
                  {"posts": all_posts, "categories": Category.objects.all(), "tags": Tag.objects.all()})


def clear_filter(request):
    return redirect('all_posts')


@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user.profile
            post.save()
            post_form.save_m2m()
            return redirect('all_posts')
    else:
        post_form = PostForm()
    return render(request, 'manage_post.html', {'form': post_form, 'create': True})


@login_required
def update_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('all_posts')
    else:
        post_form = PostForm(instance=post)
    return render(request, 'manage_post.html', {'form': post_form, 'create': False})


@login_required
def del_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('all_posts')


@login_required
def manage_profile(request):
    profile = request.user.profile
    return render(request, "profile.html", {'profile': profile})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form})


def show_comments(request, post_id):
    comments = Comment.objects.filter(post=post_id)
    return render(request, 'comments.html', {'comments': comments, 'post_id': post_id})


@login_required
def add_comments(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(content=content, author=request.user.profile, post=post)
        return redirect('show_comments', post_id=post_id)
    else:
        return render(request, 'comments.html', context={'post_id': post_id})


@login_required
def del_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    messages.info(request, "Comment Deleted Successfully!")
    return redirect('show_comments', post_id=comment.post.id)


@api_view(['GET', 'POST'])
def posts(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 4
        result_page = paginator.paginate_queryset(posts, request)
        post_serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(post_serializer.data)

    if request.method == 'POST':
        post_serializer = PostSerializer(data=request.data)
        if post_serializer.is_valid():
            post_serializer.save()
            return redirect('posts')
        else:
            return Response(post_serializer.errors)


@api_view(['GET', 'POST', 'DELETE'])
def get_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'GET':
        post_serializer = PostSerializer(post, many=False)
        return Response(post_serializer.data)
    if request.method == 'POST':
        post_serializer = PostSerializer(data=request.data, instance=post)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data)
        else:
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        post.delete()
        return HttpResponseRedirect(redirect_to=reverse('posts'))


@api_view(['GET'])
def categories(request):
    categories = Category.objects.all()
    category_serializer = CategorySerializer(categories, many=True)
    return Response(category_serializer.data)


@api_view(['GET'])
def tags(request):
    tags = Tag.objects.all()
    tag_serializer = TagSerializer(tags, many=True)
    return Response(tag_serializer.data)


@api_view(['GET', 'POST'])
def comments(request):
    if request.method == 'GET':
        comments = Comment.objects.all()
        comment_serializer = CommentSerializer(comments, many=True)
        return Response(comment_serializer.data)
    if request.method == 'POST':
        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return HttpResponseRedirect(redirect_to=reverse('comments'))
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'GET':
        comment_serializer = CommentSerializer(comment, many=False)
        return Response(comment_serializer.data)
    if request.method == 'DELETE':
        comment.delete()
        return Response("Comment Deleted Successfully!")
