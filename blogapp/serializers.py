from rest_framework import serializers

from blogapp.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        # fields = ('title', 'content', 'author', 'categories', 'tags', 'created_at','updated_at')