from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import User, Post, Comment,Category
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=['email', 'name', 'password', 'password2', 'tc', 'image', 'lati', 'long','cityName','description']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
  # owner = serializers.ReadOnlyField(source='owner.email')
  # post_id = serializers.IntegerField(source='post.id')
  # post = serializers.
  # posts = serializers.SlugRelatedField( many=True,slug_field='id', read_only=True,)
  # post_img=serializers.ReadOnlyField(source='posts.image_url')

  # owner = serializers.ReadOnlyField(source='owner.email')
  # post_id = serializers.IntegerField(source='post.id')
  # post = serializers.

  class Meta:
    model = User
    fields = ['id', 'email', 'name', 'image','lati', 'long','cityName','description']


class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email=email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
      print('Password Reset Link', link)
      # Send EMail
      body = 'Click Following Link to Reset Your Password '+link
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
      # Util.send_email(data)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')

class PostSerializer(serializers.ModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.email')
  comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

  class Meta:
    model = Post
    fields = ['id', 'title', 'body', 'owner','image_url','place', 'comments', 'long', 'lati','categories', "datetim", 'date','time','categories','cityName','likes']

class CommentSerializer(serializers.ModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.email')
  posts = serializers.ReadOnlyField(source='post.long')


  class Meta:
    model = Comment
    fields = ['id', 'file', 'owner', 'post','posts']

class CategorySerializer(serializers.ModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.email')
  posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


  class Meta:
    model = Category
    fields = ['id', 'name', 'owner', 'posts', ]
class UserDetailListSerializer(serializers.ModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.email')
  post_id = serializers.IntegerField(source='post.id')
  post_img=serializers.ImageField(source='post.image_url')
  class Meta:
    model = User
    fields = ['id', 'name', 'post_id', 'post_img']
class PostListSerializer(serializers.ModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.name')
  comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
  user_img = serializers.ImageField(source='owner.image')
  userid = serializers.IntegerField(source="owner.id")
  categories = serializers.SlugRelatedField( many=True,slug_field='name', read_only=True,)
  read_by_you =serializers.BooleanField()
  # read_by_you =SerializerMethodField()
  class Meta:
    model = Post

    fields = ['id', 'title', 'body', 'owner','image_url','place', 'comments', 'long', 'lati','categories', "date","user_img","userid", 'time','cityName','likes','read_by_you']
    def save(self):
      user = self.context['request'].user
      return  user


class PostListLolSerializer(serializers.ModelSerializer):
  # posts = serializers.SlugRelatedField(slug_field='image_url')

  class Meta:
    model = User
    fields = ['id', 'email', 'name', 'image', 'description' ]
class UserPostList(serializers.ModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.name')
  comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
  userid = serializers.IntegerField(source="owner.id")
  categories = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True, )

  class Meta:
    model = Post
    fields = ['id', 'title', 'body', 'owner', 'image_url', 'place', 'comments', 'long', 'lati', 'categories', "date", "userid", 'time', ]

class LikeSerializer(serializers.ModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.name')

  class Meta:
    model = Post
    fields = ['id', 'likes']
class LikedPostsSerializer(serializers.ModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.name')
  comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
  userid = serializers.IntegerField(source="owner.id")
  categories = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True, )

  class Meta:
    model = Post
    fields = ['id', 'title', 'body', 'owner','image_url','place', 'comments', 'long', 'lati','categories', "date","userid", 'time','cityName','likes']
class ChangeUserSerializer(serializers.ModelSerializer):
  cityName = serializers.CharField(max_length=255,  write_only=True)

  class Meta:
    model = User
    fields = ['id', 'email', 'name', 'cityName','description' ]