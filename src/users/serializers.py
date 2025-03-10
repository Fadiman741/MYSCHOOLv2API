from rest_framework import serializers
from .models import ( User, Grade, Subject)

from .models import Announcement, AnnouncementLike ,AnnouncementComment, AnnouncementCommentLike, AnnouncementReply, AnnouncementReplyLike

from .models import Post,PostLike,PostReplyLike,PostReply,PostComment

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

# =============   GRADES AND SUBJECTS  =========================================================================================
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    grade = GradeSerializer(read_only=True)
    class Meta:
        model = Subject
        fields = '__all__'

# ============= ANNOUCEMENT ========================================================================================================
class AnnouncementCommentSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = AnnouncementComment
        fields = ['id', 'user', 'content', 'image', 'video', 'created_at', 'parent_comment', 'like_count', 'replies']

    def get_like_count(self, obj):
        """Returns the total number of likes for this comment."""
        return obj.like_count

    def get_replies(self, obj):
        """Returns all replies for this comment."""
        replies = obj.announcement_replies.all()
        return AnnouncementReplySerializer(replies, many=True, context=self.context).data

    
class AnnouncementSerializer(serializers.ModelSerializer):
    like_count = serializers.ReadOnlyField()
    comment_count = serializers.ReadOnlyField()
    user_has_liked = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    comments = AnnouncementCommentSerializer(many=True, read_only=True, source="announcement_comments")

    class Meta:
        model = Announcement
        fields = [
            'id', 'user', 'description', 'title', 'datecreated', 'image', 'video',
            'tagged_friends', 'feeling', 'like_count', 'comment_count', 'user_has_liked', 'comments'
        ]

    def get_user_has_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.announcement_likes.filter(user=request.user).exists()
        return False

class AnnouncementLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementLike
        fields = ['id', 'user', 'announcement', 'created_at']



class AnnouncementCommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementCommentLike
        fields = ['id', 'user', 'comment', 'created_at']

class AnnouncementReplySerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = AnnouncementReply
        fields = ['id', 'user', 'comment', 'content', 'image', 'video', 'created_at', 'like_count', 'user_has_liked']

    def get_like_count(self, obj):
        """Returns the total number of likes for this reply."""
        return obj.like_count

    def get_user_has_liked(self, obj):
        """Checks if the authenticated user has liked this reply."""
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.announcement_reply_likes.filter(user=request.user).exists()
        return False

class AnnouncementReplyLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementReplyLike
        fields = ['id', 'user', 'reply', 'created_at']


# ============= POST ========================================================================================================
class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['id', 'user', 'post', 'created_at']

class PostReplySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()

    class Meta:
        model = PostReply
        fields = [
            'id', 'user', 'content', 'created_at', 'like_count', 'user_has_liked'
        ]

    def get_like_count(self, obj):
        # Return the total number of likes for the reply
        return obj.like_count

    def get_user_has_liked(self, obj):
        # Check if the authenticated user has liked the reply
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.post_reply_likes.filter(user=request.user).exists()
        return False
class PostCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = [
            'id', 'user', 'content', 'created_at', 'replies', 'like_count', 'user_has_liked'
        ]

    def get_replies(self, obj):
        # Fetch all replies for this comment
        replies = obj.replies.all()
        return PostReplySerializer(replies, many=True, context=self.context).data

    def get_like_count(self, obj):
        # Return the total number of likes for the comment
        return obj.like_count

    def get_user_has_liked(self, obj):
        # Check if the authenticated user has liked the comment
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.post_comment_likes.filter(user=request.user).exists()
        return False
class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post_likes = PostLikeSerializer(many=True, read_only=True)
    user_has_liked = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'content', 'created_at', 'comments', 'grade', 'subject',
            'image', 'feeling', 'tagged_friends', 'post_likes', 'like_count', 'user_has_liked'
        ]

    def get_comments(self, obj):
        # Fetch top-level comments (comments without a parent)
        comments = obj.post_comments.filter(parent_comment__isnull=True)
        return PostCommentSerializer(comments, many=True, context=self.context).data

    def get_like_count(self, obj):
        # Return the total number of likes for the post
        return obj.like_count

    def get_user_has_liked(self, obj):
        # Check if the authenticated user has liked the post
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.post_likes.filter(user=request.user).exists()
        return False

# ============= REPLY ========================================================================================================

class ReplyLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReplyLike
        fields = ['id', 'user', 'reply', 'created_at']

# class ReplySerializer(serializers.ModelSerializer):
#     reply_likes = ReplyLikeSerializer(many=True, read_only=True)
#     like_count = serializers.SerializerMethodField()
#     class Meta:
#         model = PostReply
#         fields = ['id', 'user', 'comment', 'content', 'created_at']

# # ============= ANNOUCEMENT COMMENTS ========================================================================================================




























# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = "__all__"

# ===============================================================================================================================
