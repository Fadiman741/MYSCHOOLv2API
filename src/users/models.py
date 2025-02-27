import datetime
import random
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import random
import cloudinary.models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=255, unique=True)
    datecreated = models.DateTimeField(auto_now_add=True)
    occupation = models.CharField(max_length=100, null=True)
    schoolname = models.CharField(max_length=100, null=True)
    profile_picture = cloudinary.models.CloudinaryField('', blank=True, null=True)
    years_of_experience = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    subjects = models.CharField(max_length=255, blank=True, null=True)
    school = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="announcements", blank=True) 

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.username:
            random_number = random.randint(100, 999)
            self.username = f"{self.first_name}{self.last_name}{random_number}"
        super().save(*args, **kwargs)


class Announcement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, related_name="announcements", on_delete=models.CASCADE
    )
    description = models.TextField()
    title = models.CharField(max_length=100,null=True, blank=True)
    datecreated = models.DateTimeField(auto_now_add=True)
    image = cloudinary.models.CloudinaryField("", null=True, blank=True)
    video = cloudinary.models.CloudinaryField("", null=True, blank=True)
    tagged_friends = models.ManyToManyField(User, related_name="tagged_announcements", blank=True)
    feeling = models.CharField(
        max_length=50,
        choices=[
            ("happy", "Happy"),
            ("sad", "Sad"),
            ("excited", "Excited"),
            ("angry", "Angry"),
        ],
        blank=True,
    )

    def __str__(self):
        return f"{self.user} : {self.title} "

class Grade(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} "

class Subject(models.Model):
    name = models.CharField(max_length=100)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}  :  {self.grade} "
class Subtopic(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0, null=True)
    # unlikes = models.IntegerField(default=0, null=True)
    comments = models.IntegerField(default=0, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    image = cloudinary.models.CloudinaryField('', null=True, blank=True)  # For post image
    feeling = models.CharField(max_length=50, null=True, blank=True)  # For feeling (e.g., happy, sad)
    tagged_friends = models.ManyToManyField(User, related_name="tagged_posts", blank=True)  # For tagging friends

    def __str__(self):
        return f"{self.user} : {self.content}"

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    likes = models.IntegerField( default=0, null=True)
    unlikes = models.IntegerField(default=0, null=True)
    # comments = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Comment by {} - {}'.format(self.user, self.content)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=255, default="Notification")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=0, null=False)

    def __str__(self):
        return self.content

# ===========================================================================================================================================================
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

# Create your models here.

class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']

        def __str__(self):
            return self.unique_together


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
# ------------------------------------------------------------------------------------------------------
