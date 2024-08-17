# serializers.py

from rest_framework import serializers
from .models import User, Post, Comment
from django.contrib.auth.hashers import make_password

class UserLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
        
class UserCommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
        }
class CommentSerializer(serializers.ModelSerializer):
    commented_by = UserCommentSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'post', 'commented_by', 'created', 'updated']
        
class PostSerializer(serializers.ModelSerializer):
    posted_by = UserCommentSerializer(read_only=True)
    likes = UserLikesSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'content', 'posted_by', 'likes', 'created', 'updated', 'comments']
        
class UserSerializer(serializers.ModelSerializer):
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    following = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    posts = PostSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'profile_pic', 'cover_pic', 'likes', 'followers', 'following', 'password', 'posts']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])  # Use set_password for hashing
        user.save()
        return user

