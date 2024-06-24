from django.shortcuts import render, redirect

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view

from blogapp.models import Post
from blogapp.serializers import PostSerializer


# Create your views here.
def register(request):
    if request.user.is_authenticated:
        pass
    else:
        pass


def api_login(request):
    pass


def api_logout(request):
    pass


@api_view(['GET', 'POST'])
def get_posts(request):
    if request.method == 'GET':
        posts = Post.object.all()
        post_serializer = PostSerializer(posts, many=True)
        return Response(post_serializer.data)
    if request.method == 'POST':
        post_serializer = PostSerializer(data=request.data)
        if post_serializer.is_valid():
            post_serializer.save()
            return redirect('get-posts')


@api_view(['GET', 'POST', 'DELETE'])
def get_post(request, post_id):
    post = Post.object.get(id=post_id)
    if request.method == 'GET':
        post_serializer = PostSerializer(post, many=False)
        return Response(post_serializer.data)
    if request.method == 'POST':
        post_serializer = PostSerializer(data=request.data, instance=post)
        if post_serializer.is_valid():
            post_serializer.save()
            return redirect('get-posts')

    if request.method == 'DELETE':
        post.delete()
        return Response("Post Deleted Successfully!")
