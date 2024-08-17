from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User, Post, Comment
from .serializer import UserSerializer, PostSerializer, CommentSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponseNotFound
from .chain import chainResponse

class DeleteUserView(APIView):
    
    def delete(self, request, username):
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response({'message': 'User deleted successfully.'}, status=status.HTTP_200_OK)

def custom_404_view(request, exception):
    # You can customize the template and context as needed
    return HttpResponseNotFound(render(request, '404.html'))
    
class UserListCreateView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            refresh = RefreshToken.for_user(serializer)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostListCreateView(APIView):

    def get(self, request):
        posts = Post.objects.all().order_by('-created')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(posted_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(APIView):

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = Post.objects.get(pk=pk)
        if post.posted_by != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.posted_by != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentListCreateView(APIView):

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(commented_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):

    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.commented_by != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.commented_by != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class HomePageView(APIView):
    
    def get(self, request):
        print(request.user)
        return render(request, 'home.html')#, {'user_data': user_info})

class RegisterUserView(APIView):
    def get(self, request):
        # Render the index page or login page
        return render(request, 'register.html')
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
    def get(self, request):
        # Render the index page or login page
        return render(request, 'index.html')
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
          
            refresh = RefreshToken.for_user(user)
            return Response({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
                "profile_pic": user.profile_pic.url if user.profile_pic else None,
                "cover_pic": user.cover_pic.url if user.cover_pic else None,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LikePostView(APIView):

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            message = 'Post unliked'
        else:
            post.likes.add(user)
            message = 'Post liked'

        post.save()
        return Response({'message': message}, status=status.HTTP_200_OK)
    
class ProfileView(APIView):
    def get(self,request):
        return render(request, 'profile.html')
    
    def post(self,request,username):
        user = get_object_or_404(User, username=username)
        request_user = request.user
        if user:
            is_following = user.followers.filter(id=request_user.id).exists()
            return Response({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
                "profile_pic": user.profile_pic.url if user.profile_pic else None,
                "cover_pic": user.cover_pic.url if user.cover_pic else None,
                "followers_count": user.followers.count(),  # Count followers
                "following_count": user.following.count(),
                "is_following": is_following,
            
            },status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
class UserPostsView(APIView):
    
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(posted_by=user).order_by('-created')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class FollowUnfollowView(APIView):
    

    def post(self, request, username):
        to_follow_user = get_object_or_404(User, username=username)
        current_user = request.user

        if current_user == to_follow_user:
            return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

        if to_follow_user in current_user.following.all():
            current_user.following.remove(to_follow_user)
            message = 'Unfollowed successfully'
        else:
            current_user.following.add(to_follow_user)
            message = 'Followed successfully'

        return Response({'message': message}, status=status.HTTP_200_OK)
    
class UpdateProfilePictureView(APIView):

    def post(self, request):
        user = request.user
        profile_pic = request.FILES.get('profile_pic')
        
        if not profile_pic :
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        if profile_pic:
            user.profile_pic = profile_pic

        user.save()
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UpdateCoverPictureView(APIView):
    def post(self, request):
        user = request.user
        cover_pic = request.FILES.get('cover_pic')
        
        if not cover_pic:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        user.cover_pic = cover_pic
        user.save()
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GPTView(APIView):
    
    def post(self, request):
        try:
            data = request.data
            if data:
                response = {'response':chainResponse(data)}
                print(response)
                return Response(response, status=status.HTTP_200_OK)
            return Response({'error': 'No data provided'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error in GPTView: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        