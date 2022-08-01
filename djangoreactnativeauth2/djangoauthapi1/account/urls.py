from django.urls import path, re_path
from .views import SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserProfileView, UserRegistrationView,\
    UserPasswordResetView, PostList, PostDetail,\
    CommentList,CommentDetail,\
    CategoryList,CategoryDetail,\
    MyPostList, PostCat, UserList, UserDetail,UserDetailList, PostListView,\
    MyPostUserList, EditMyProfile, AddLikeUnlikeView,MyLikedPostUserList,UserChangeView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change/', UserChangeView.as_view()),

    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('posts/', PostListView.as_view()),
    path('postsall/', PostList.as_view()),

    path('posts/<int:pk>/', PostDetail.as_view()),
    path('comments/', CommentList.as_view()),
    path('comments/<int:pk>/', CommentDetail.as_view()),
    path('categories/', CategoryList.as_view()),
    path('categories/<int:pk>/', CategoryDetail.as_view()),
    path('myposts/', MyPostList.as_view()),
    path('jopa/', MyPostUserList.as_view()),
    path('like/unlike/<int:post_id>', AddLikeUnlikeView.as_view()),
    path('liked/', MyLikedPostUserList.as_view()),

    re_path('popa', PostCat.as_view()),

    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('edit/', EditMyProfile.as_view()),

]