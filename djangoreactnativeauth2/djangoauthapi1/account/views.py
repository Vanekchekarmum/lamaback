from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer,\
  UserLoginSerializer, UserPasswordResetSerializer,\
  UserProfileSerializer, UserRegistrationSerializer, PostSerializer,\
  CommentSerializer,CategorySerializer,UserDetailListSerializer, PostListSerializer,\
  PostListLolSerializer, UserPostList
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment, Category, User
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  parser_classes = (MultiPartParser, FormParser)

  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  parser_classes = (MultiPartParser, FormParser)
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)



class PostList(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Post.objects.all().order_by('-id')
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categories']
    def perform_create(self, serializer):
      serializer.save(owner=self.request.user)


class PostListView(generics.ListAPIView):
  # permission_classes = [IsAuthenticated]
  queryset = Post.objects.all().order_by('-id')
  serializer_class = PostListSerializer
  parser_classes = (MultiPartParser, FormParser)
  filter_backends = [DjangoFilterBackend]
  filterset_fields = ['categories']


  def perform_create(self, serializer):
    serializer.save(categories=self.request.categories)
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
class UserList(generics.ListCreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserProfileSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = User.objects.all()
  serializer_class = UserProfileSerializer
class UserDetailList(generics.RetrieveUpdateDestroyAPIView):
  queryset = User.objects.all()
  serializer_class = UserDetailListSerializer

class CommentList(generics.ListCreateAPIView):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer
  parser_classes = (MultiPartParser, FormParser)
  filter_backends = [DjangoFilterBackend]
  filterset_fields = ['post']
  # permission_classes = [IsAuthenticated]

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer
  # permission_classes = [IsAuthenticated]
# class PostOwnerList(generics.ListCreateAPIView):
#     permission_classes = []
#   queryset = Post.objects.all().order_by('-id')
#   serializer_class = PostSerializer
#   parser_classes = (MultiPartParser, FormParser)
#
#   def perform_create(self, serializer):
#     serializer.save(owner=self.request.user)
class CategoryList(generics.ListCreateAPIView):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer


  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer


class MyPostList(generics.ListAPIView):

  serializer_class = PostListLolSerializer
  def list(self, request, *args, **kwargs):
    self.object_list = self.filter_queryset(self.get_queryset())
    serializer = self.get_serializer(self.object_list, many=True)
    return Response({'data': serializer.data})

  def get_queryset(self):
    return User.objects.all().filter(email=self.request.user)
class MyPostUserList(generics.ListAPIView):

  serializer_class = UserPostList

  def get_queryset(self):
    return Post.objects.all().filter(owner=self.request.user)


class PostCat(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = PostSerializer

  def get_queryset(self):

    title = "title"
    return Post.objects.filter(title=title)
class EditMyProfile(generics.UpdateAPIView):

  serializer_class = PostListLolSerializer

  def get_queryset(self):
    return User.objects.all().filter(email=self.request.user)