from rest_framework import serializers
from .models import (
    User,
    Announcement,
    Post,
    Comment,
    Message,
    UserProfile,
    Notification,
    Grade,
    Subject,
    Subtopic,
    Thread

)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'username', 'email', 'datecreated', 'occupation', 
            'schoolname', 'profile_picture', 'years_of_experience', 'role', 'subjects', 
            'school', 'location', 'languages', 'facebook', 'twitter', 'linkedin', 'phone', 'tags'
        ]
        extra_kwargs = {"password": {"write_only": True}}


class AnnouncementSerialiazer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Announcement
        fields = ["id", "user", "title", "description", "datecreated","image",
            "video",
            "tagged_friends",
            "feeling"]
        ordering = ["-datecreated"]

    def __str__(self):
        return self.user

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class SubtopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtopic
        fields = '__all__'



class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # content = serializers.CharField()
    class Meta:
        model = Post
        fields = [
            'id', 
            'user', 
            'content', 
            'created_at', 
            'likes', 
            'comments', 
            'grade', 
            'subject', 
            'image', 
            'feeling', 
            'tagged_friends'
        ]
        read_only_fields = ['user', 'created_at', 'likes', 'comments']



















# class PostSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     # grade = GradeSerializer()
#     # Subject = SubjectSerializer()
    
#     class Meta:
        
#         model = Post
#         # contents =serializers.CharField()
#         fields = "__all__"
#         # ordering = ["-datecreated"]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    post = PostSerializer()

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "post",
            "content",
            "created_at",
            "likes",
            "unlikes",
            # "comments",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(
        many=False, slug_field="username", queryset=User.objects.all()
    )
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # receiver = serializers.SlugRelatedField(
    #     many=False, slug_field="username", queryset=User.objects.all()
    # )

    class Meta:
        model = Message
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Notification
        fields = "__all__"

# ================================================================================================================================
class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = "__all__"
# -------------------------------------------------------------------------------------------------------------------------
