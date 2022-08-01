from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)
#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, name, tc,image,cityName,lati,long,description, password=None, password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          name=name,
          tc=tc,
          image=image,
          cityName=cityName,
          lati=lati,
          long=long,
          description=description
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name, tc,image,cityName,lati,long,description, password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
          name=name,
          tc=tc,
          image=image,
          cityName=cityName,
          lati=lati,
          long=long,
          description=description
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

#  Custom User Model
class User(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  name = models.CharField(max_length=200)

  tc = models.BooleanField()
  image = models.ImageField(upload_to=upload_to, blank=True, null=True)
  cityName = models.TextField(blank=True, default='')
  description = models.TextField(blank=True, default='')

  long = models.FloatField(blank=True)
  lati = models.FloatField(blank=True)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name', 'tc']

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin

class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    body = models.TextField(blank=True, default='')
    owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
    place = models.TextField(blank=True, default='')
    cityName = models.TextField(blank=True, default='')
    likes = models.ManyToManyField('User',blank=True,related_name='likes')

    long = models.FloatField(blank=True)
    lati = models.FloatField(blank=True)
    datetim= models.DateTimeField(blank=True, null=True)
    date = models.CharField(max_length=100, blank=True, default='')
    time = models.CharField(max_length=100, blank=True, default='')


    class Meta:
        ordering = ['created']

class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(blank=False, null=False)
    # body = models.FileField(upload_to=upload_to,blank=False,null=True)
    owner = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']
class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    posts = models.ManyToManyField(Post, related_name='categories', blank=True)

    class Meta:
        verbose_name_plural = 'categories'

