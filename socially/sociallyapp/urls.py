from django.urls import path
from .views import UserListCreateView, UserDetailView, PostListCreateView, PostDetailView, CommentListCreateView, CommentDetailView, RegisterUserView, LoginUserView, HomePageView, LikePostView, ProfileView, UserPostsView, FollowUnfollowView, UpdateProfilePictureView, UpdateCoverPictureView, GPTView, DeleteUserView

urlpatterns = [
    path('', LoginUserView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('home/',HomePageView.as_view(), name='home'),
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('profile/',ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/',ProfileView.as_view(), name='profile'),
    path('user/<str:username>/posts/', UserPostsView.as_view(),name="user-posts"),
    path('follow/<str:username>/',FollowUnfollowView.as_view(),name="follow-unfollow"),
    path('update/profile-pic/', UpdateProfilePictureView.as_view(), name='update-profile-pic'),
    path('update/cover-pic/', UpdateCoverPictureView.as_view(), name='update-cover-pic'),
    path('GPT/', GPTView.as_view(), name='gpt'),
    path('delete-user/<str:username>/', DeleteUserView.as_view(), name='delete-user')
]
handler404 = 'sociallyapp.views.custom_404_view'