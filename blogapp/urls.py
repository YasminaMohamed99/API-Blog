from django.urls import path

from blogapp import views

urlpatterns = [
    path('api/register', views.register, name='register'),
    path('api/login', views.api_login, name='login'),
    path('api/logout', views.api_logout, name='logout'),

    path('api/posts', views.get_posts, name='get-posts'),
    path('api/posts/<id>', views.get_post, name='get-post'),

]