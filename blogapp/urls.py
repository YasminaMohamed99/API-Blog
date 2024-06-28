from django.urls import path

from blogapp import views



urlpatterns = [
    path('', views.list_posts, name='all_posts'),
    path('register/', views.sign_up, name='register'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('profile/', views.manage_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('post/<int:post_id>/comments/', views.show_comments, name='show_comments'),
    path('post/<int:post_id>/comments/add_comments/', views.add_comments, name='add_comments'),
    path('delete_comments/<int:comment_id>', views.del_comment, name='delete_comment'),
    path('create_post/', views.create_post, name='create_post'),
    path('update_post/<int:post_id>', views.update_post, name='update_post'),
    path('delete_post/<int:post_id>', views.del_post, name='delete_post'),
    path('search/', views.search, name='search_posts'),
    path('apply_filter', views.apply_filter, name='apply_filter'),
    path('clear_filter', views.clear_filter, name='clear_filter'),

    path('api/post/', views.posts, name='posts'),
    path('api/posts/<post_id>/', views.get_post, name='get-post'),
    path('api/categories/', views.categories, name='categories'),
    path('api/tags/', views.tags, name='tags'),
    path('api/comments/', views.comments, name='comments'),
    path('api/comments/<comment_id>/', views.delete_comment, name='delete-comment'),

]