from django.urls import path

from blogapp import views

urlpatterns = [
    path('api/register', views.register, name='register'),
    path('api/login', views.api_login, name='login'),
    path('api/logout', views.api_logout, name='logout'),

    path('api/posts/', views.get_posts, name='get-posts'),
    path('api/posts/<post_id>/', views.get_post, name='get-post'),
    path('api/categories/', views.get_categories, name='get-categories'),
    path('api/tags/', views.get_tags, name='get-tags'),
    path('api/comments/', views.get_comments, name='get-comments'),
    path('api/comments/<comment_id>/', views.delete_comment, name='delete-comment'),

]