import datetime
import random
import uuid
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

# =========  GRADES & SUBJECTS ==================================================================================
class Grade(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.name} "
class Subject(models.Model):
    name = models.CharField(max_length=100)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}  :  {self.grade} "
# =========  ANNOUCEMENT ======================================================================================
class Announcement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="announcements", on_delete=models.CASCADE)
    description = models.TextField()
    title = models.CharField(max_length=100, null=True, blank=True)
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
        return f"{self.user} : {self.title}"

    @property
    def like_count(self):
        """Returns the total number of likes for this announcement."""
        return self.announcement_likes.count()
class AnnouncementLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="announcement_likes")
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="announcement_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'announcement')  # Ensures a user can like an announcement only once

    def __str__(self):
        return f"{self.user} liked {self.announcement}"  
# =========  ANNOUCEMENT COMMENT ==============================================================================
class AnnouncementComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="announcement_comments")
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="announcement_comments")
    content = models.TextField()
    image = cloudinary.models.CloudinaryField("", null=True, blank=True)
    video = cloudinary.models.CloudinaryField("", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")  # For nested comments

    def __str__(self):
        return f"{self.user} commented on {self.announcement}: {self.content}"

    @property
    def like_count(self):
        """Returns the total number of likes for this comment."""
        return self.announcement_comment_likes.count()
class AnnouncementCommentLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="announcement_comment_likes")
    comment = models.ForeignKey(AnnouncementComment, on_delete=models.CASCADE, related_name="announcement_comment_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')  # Ensures a user can like a comment only once

    def __str__(self):
        return f"{self.user} liked {self.comment}"
# ========= ANNOUCEMENT REPLY =================================================================================
class AnnouncementReply(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="announcement_replies")
    comment = models.ForeignKey('AnnouncementComment', on_delete=models.CASCADE, related_name="replies")
    content = models.TextField()
    image = cloudinary.models.CloudinaryField("", null=True, blank=True)
    video = cloudinary.models.CloudinaryField("", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} replied to {self.comment}: {self.content}"

    @property
    def like_count(self):
        """Returns the total number of likes for this reply."""
        return self.announcement_reply_likes.count()
class AnnouncementReplyLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="announcement_reply_likes")
    reply = models.ForeignKey(AnnouncementReply, on_delete=models.CASCADE, related_name="announcement_reply_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'reply')  # Ensures a user can like a reply only once

    def __str__(self):
        return f"{self.user} liked {self.reply}"
    
# ===============================================================================================================






















































































































# ==========    POST  ===========================================================================================
# class Post(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
#     content = models.TextField(null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     comments = models.IntegerField(default=0, null=True)
#     grade = models.ForeignKey('Grade', on_delete=models.CASCADE, null=True)  # Assuming Grade is another model
#     subject = models.ForeignKey('Subject', on_delete=models.CASCADE, null=True)  # Assuming Subject is another model
#     image = cloudinary.models.CloudinaryField('', null=True, blank=True)  # For post image
#     feeling = models.CharField(max_length=50, null=True, blank=True)  # For feeling (e.g., happy, sad)
#     tagged_friends = models.ManyToManyField(User, related_name="tagged_posts", blank=True)  # For tagging friends

#     def __str__(self):
#         return f"{self.user} : {self.content}"

#     @property
#     def like_count(self):
#         """Returns the total number of likes for this post."""
#         return self.post_likes.count()
# class PostLike(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_likes")
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")
#     created_at = models.DateTimeField(auto_now_add=True)
#     class Meta:
#         unique_together = ('user', 'post')  # Ensures a user can like a post only once

#     def __str__(self):
#         return f"{self.user} liked {self.post}"
# # ===========  POST COMMMENT ====================================================================================
# class PostComment(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_comments")
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")  # For nested comments

#     def __str__(self):
#         return f"{self.user} commented on {self.post}: {self.content}"

#     @property
#     def like_count(self):
#         """Returns the total number of likes for this comment."""
#         return self.post_comment_likes.count()
# class PostCommentLike(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_comment_likes")
#     comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name="post_comment_likes")
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'comment')  # Ensures a user can like a comment only once

#     def __str__(self):
#         return f"{self.user} liked {self.comment}"

# # ========= POST REPLY  ========================================================================================
# class PostReply(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.ForeignKey(PostComment, related_name="replies", on_delete=models.CASCADE)
#     reply = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return 'Reply by {} - {}'.format(self.user, self.reply)
# class PostReplyLike(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_likes")
#     reply = models.ForeignKey(PostReply, on_delete=models.CASCADE, related_name="reply_likes")
#     created_at = models.DateTimeField(auto_now_add=True)
#     class Meta:
#         unique_together = ('user', 'reply')  # Ensures a user can like a post only once

#     def __str__(self):
#         return f"{self.user} liked {self.reply}"
