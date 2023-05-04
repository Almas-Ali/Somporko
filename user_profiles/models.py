from django.db import models
from django.utils.timezone import now
from io import BytesIO
import PIL
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from random import sample
from string import digits
from sys import getsizeof
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


def size_calculate(height, width):
    if height <= 1200 and width <= 1200:
        h, w = height//2, width//2
    elif height <= 2000 and width <= 2000:
        h, w = height//4, width//4
    elif height <= 5000 and width <= 5000:
        h, w = height//5, width//5
    else:
        h, w = height//6, width//6
    return h, w


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_blue_badge', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            **extra_fields
        )

        user.save(using=self._db)

        return user


class User(AbstractUser, PermissionsMixin):
    is_verified = models.BooleanField(default=False)  # Email verification
    is_blue_badge = models.BooleanField(default=False)  # Blue badge
    is_active = models.BooleanField(default=True)  # Account status
    is_staff = models.BooleanField(default=False)  # Staff status
    is_superuser = models.BooleanField(default=False)  # Superuser status

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    bio = models.CharField(max_length=120, default='')
    phone = models.CharField(max_length=16, default='')
    address = models.TextField(max_length=255, default='')
    religion = models.CharField(max_length=25, default='')
    gender = models.IntegerField(default=0)
    birthday = models.DateField(default=now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    def get_image(self):
        return self.profile_image.image.url

    def set_gender(self, gender: str):
        gender: str = gender.lower()
        if gender == 'male':
            self.gender = 1
        elif gender == 'female':
            self.gender = 2
        elif gender == 'other':
            self.gender = 3
        else:
            self.gender = 0

        self.save()

    def get_gender(self):
        if self.gender == 1:
            gender: str = 'male'
        elif self.gender == 2:
            gender: str = 'female'
        elif self.gender == 3:
            gender: str = 'other'
        else:
            gender: str = 'unknown'

        return gender


class ProfileImage(models.Model):
    id = models.AutoField(verbose_name='Image id', primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='profile_image')
    image = models.ImageField(
        upload_to='profile/', blank=True, null=True, default='')

    def save(self, *args, **kwargs):
        # Opening the uploaded image
        img = Image.open(self.img)
        img = img.convert('RGB')

        output = BytesIO()

        h, w = img.size
        im = img.resize(size_calculate(h, w), Image.ANTIALIAS)

        im.save(output, format='jpeg', quality=90)

        name = ''.join(sample(digits+digits, 20))+'.jpeg'

        self.img = InMemoryUploadedFile(
            output, 'ImageField', f'{name}', 'image/jpeg', getsizeof(output), None)

        super(ProfileImage, self).save()


# Has been merged into User model
class ManageProfile(models.Model):
    bio = models.CharField(max_length=120, default='')
    sno = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, blank=False, default='')
    phone = models.CharField(max_length=16, default='')
    address = models.TextField(max_length=255, default='')
    religion = models.CharField(max_length=25, default='')
    gender = models.CharField(max_length=10, default='')
    birthday = models.DateField(default=now)

    def __str__(self):
        return str(self.sno)


class ProfilePost(models.Model):
    id = models.AutoField(verbose_name='Post id', primary_key=True)
    sno = models.CharField(default=User, max_length=30)
    feelings = models.CharField(
        max_length=50, default='', blank=True, null=True)
    img = models.ImageField(
        upload_to='post/', blank=True, null=True, default='')
    post = models.TextField(max_length=5000, default='', null=True, blank=True)
    date = models.DateTimeField(default=now)
    likes = models.ManyToManyField(
        User, related_name='ProfilePost', default=None, blank=True)
    is_profile_img = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Opening the uploaded image
        img = Image.open(self.img)
        img = img.convert('RGB')

        output = BytesIO()

        h, w = img.size
        im = img.resize(size_calculate(h, w), Image.ANTIALIAS)

        im.save(output, format='jpeg', quality=90)

        name = ''.join(sample(digits+digits, 20))+'.jpeg'

        self.img = InMemoryUploadedFile(
            output, 'ImageField', f'{name}', 'image/jpeg', getsizeof(output), None)

        super(ProfilePost, self).save()

    def __str__(self):
        return str(self.id)

    @property
    def total_likes(self):
        return self.likes.all().count()


class Comment(models.Model):
    sno = models.AutoField(primary_key=True)
    cmt = models.TextField(default='', max_length=5000)
    post = models.ForeignKey(ProfilePost, on_delete=models.CASCADE, default='')
    user = models.ForeignKey(User, related_name='user',
                             on_delete=models.CASCADE, default=None)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    time = models.DateTimeField(default=now)
    likes = models.ManyToManyField(
        User, related_name='comment_like', default=None, blank=True)

    @property
    def total_like(self):
        return self.likes.all().count()

    def __str__(self):
        return str(self.sno)

# Need to lookup dependency of this model


class UserDetail(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, default=None, blank=True)
    value = models.TextField(default='', max_length=500)
    time = models.DateTimeField(default=now)

    def __str__(self):
        return self.sno
