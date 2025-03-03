from rest_framework import serializers
from .models import ( User, Grade, Subject)

from .models import Announcement, AnnouncementLike, AnnouncementComment, AnnouncementCommentLike, AnnouncementReply, AnnouncementReplyLike

# ============= USER ========================================================================================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'username', 'email', 'datecreated', 'occupation', 
            'schoolname', 'profile_picture', 'years_of_experience', 'role', 'subjects', 
            'school', 'location', 'languages', 'facebook', 'twitter', 'linkedin', 'phone', 'tags'
        ]
        extra_kwargs = {"password": {"write_only": True}}

# ============= ANNOUCEMENT ========================================================================================================
class AnnouncementSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ['id', 'user', 'description', 'title', 'datecreated', 'image', 'video', 'tagged_friends', 'feeling', 'like_count']

    def get_like_count(self, obj):
        return obj.like_count

class AnnouncementLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementLike
        fields = ['id', 'user', 'announcement', 'created_at']

class AnnouncementCommentSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = AnnouncementComment
        fields = ['id', 'user', 'announcement', 'content', 'created_at', 'parent_comment', 'like_count']

    def get_like_count(self, obj):
        return obj.like_count

class AnnouncementCommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementCommentLike
        fields = ['id', 'user', 'comment', 'created_at']

class AnnouncementReplySerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = AnnouncementReply
        fields = ['id', 'user', 'comment', 'content', 'created_at', 'like_count']

    def get_like_count(self, obj):
        return obj.like_count

class AnnouncementReplyLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementReplyLike
        fields = ['id', 'user', 'reply', 'created_at']
    
# ============= POST ========================================================================================================
# class PostLikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PostLike
#         fields = ['id', 'user', 'post', 'created_at']

# class PostSerializer(serializers.ModelSerializer):
#     post_likes = PostLikeSerializer(many=True, read_only=True)
#     like_count = serializers.SerializerMethodField()

#     class Meta:
#         model = Post
#         fields = ['id', 'user', 'content', 'created_at', 'comments', 'grade', 'subject', 'image', 'feeling', 'tagged_friends', 'post_likes', 'like_count']

#     def get_like_count(self, obj):
#         return obj.like_count

# ============= REPLY ========================================================================================================

# class ReplyLikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ReplyLike
#         fields = ['id', 'user', 'reply', 'created_at']

# class ReplySerializer(serializers.ModelSerializer):
#     reply_likes = ReplyLikeSerializer(many=True, read_only=True)
#     like_count = serializers.SerializerMethodField()
#     class Meta:
#         model = Reply
#         fields = ['id', 'user', 'comment', 'content', 'created_at']

# # ============= ANNOUCEMENT COMMENTS ========================================================================================================

# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ['id', 'user', 'announcement', 'content', 'created_at']
























# ===============================================================================================================================
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = "__all__"

# ===============================================================================================================================
