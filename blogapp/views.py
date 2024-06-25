from django.shortcuts import render, redirect

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view

from blogapp.forms import UserForm
from blogapp.models import Post, Category, Tag, Comment
from blogapp.serializers import PostSerializer, CategorySerializer, TagSerializer, CommentSerializer


# Create your views here.
def sign_up(request):
    if request.user.is_authenticated:
        return redirect('posts')
    else:
        signup_form = UserForm()
        if request.method == 'POST':
            signup_form = UserForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                messages.info(request,"User account created successfully")
                return redirect('login')
    context = {'signup_form': signup_form}
    return render(request, 'templates/signup.html', context)


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('posts')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            passwd = request.POST.get('password')
            user = authenticate(username=name, password=passwd)
            if user is not None:
                login(request, user)
                if request.GET.get('next') is not None:
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('home')
            else:
                messages.info(request, 'User name or password is incorrect')
        return render(request, 'templates/login.html')


def sign_out(request):
    logout(request)
    return redirect('login')


@api_view(['GET', 'POST'])
def posts(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        post_serializer = PostSerializer(posts, many=True)
        return Response(post_serializer.data)
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
    print(post)
    if request.method == 'GET':
        post_serializer = PostSerializer(post, many=False)
        return Response(post_serializer.data)
    if request.method == 'POST':
        post_serializer = PostSerializer(data=request.data, instance=post)
        if post_serializer.is_valid():
            post_serializer.save()
            return redirect('posts')
        else:
            return Response(post_serializer.errors)

    if request.method == 'DELETE':
        post.delete()
        return Response("Post Deleted Successfully!")


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
    if request.method == 'Post':
        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return redirect('comments')


@api_view(['GET', 'DELETE'])
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'GET':
        comment_serializer = CommentSerializer(comment, many=False)
        return Response(comment_serializer.data)
    if request.method == 'DELETE':
        comment.delete()
        return Response("Comment Deleted Successfully!")
