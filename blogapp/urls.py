from django.urls import path

from blogapp import views

urlpatterns = [
    path('sign-up', views.sign_up, name='register'),
    path('sign-in', views.sign_in, name='login'),
    path('logout', views.sign_out, name='logout'),

    path('api/post/', views.posts, name='posts'),
    path('api/posts/<post_id>/', views.get_post, name='get-post'),
    path('api/categories/', views.categories, name='categories'),
    path('api/tags/', views.tags, name='tags'),
    path('api/comments/', views.comments, name='comments'),
    path('api/comments/<comment_id>/', views.delete_comment, name='delete-comment'),

]