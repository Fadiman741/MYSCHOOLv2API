import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
# import openai
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from users.models import Announcement,Grade, Subject, Subtopic, Notification, User, Post, Message, Comment

from django.contrib.auth import authenticate, login, logout
from .serializers import (
    UserSerializer,
    AnnouncementSerialiazer,
    GradeSerializer, SubjectSerializer, SubtopicSerializer,
    PostSerializer,
    CommentSerializer,
    NotificationSerializer,
    MessageSerializer,
)

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# from users.models import Announcement,Message ,Post
# # from users.serializers import AnnouncementSerialiazer , MessageSerializer,PostSerializer


# ======================AUTHENTICATION========================================


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data["password"])
        user.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    else:
        return Response({'error': 'User not authenticated'})

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_current_user(request):
    serializer = UserSerializer(request.user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "Email": user.email,
                "Occupation": user.occupation,
            }
        )
    return Response({"error": "Invalid credentials"}, status=401)


@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response({"success": "Logged out successfully"})


# ======================ANNOUNCEMENT========================================


@api_view(["GET"])
@permission_classes([AllowAny])
def announcement_list(request):
    announcement = Announcement.objects.all()  # complex data
    serializer = AnnouncementSerialiazer(announcement, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_announcement(request):
    user = request.user  # Assuming you are using authentication
    serializer = AnnouncementSerialiazer(data=request.data)
    Announcement.objects.create(**request.data, user=user)

    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data)
    else:
        return Response(serializer.errors)

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def get_announcement(request, pk=id):
    announcement = Announcement.objects.get(pk=pk)
    if request.method == "GET":
        serializer = AnnouncementSerialiazer(announcement)
        return Response(serializer.data)
    
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
def update_announcement(request, pk=id):
    announcement = Announcement.objects.get(pk=pk)
    if request.method == "GET":
        serializer = AnnouncementSerialiazer(announcement)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = AnnouncementSerialiazer(announcement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method == "DELETE":
        announcement.delete()
        return Response("Announcement deleted successfull")

# ==============================DROP DOWN==============================

@api_view(['GET'])
@permission_classes([AllowAny])
def grade_subject_list(request):
    grades = Grade.objects.all()
    data = []

    for grade in grades:
        subjects = grade.subject_set.all()
        subjects_list = [{'id': subject.id, 'name': subject.name} for subject in subjects]
        data.append({
            'id': grade.id,
            'name': grade.name,
            'subjects': subjects_list
        })

    return Response(data)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def grade_list(request):
    if request.method == 'GET':
        grades = Grade.objects.all()
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GradeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def grade_detail(request, pk):
    try:
        grade = Grade.objects.get(pk=pk)
    except Grade.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GradeSerializer(grade)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = GradeSerializer(grade, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        grade.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def subject_list(request):
    if request.method == 'GET':
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def subject_detail(request, pk):
    try:
        subject = Subject.objects.get(pk=pk)
    except Subject.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SubjectSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def subtopic_list(request):
    if request.method == 'GET':
        subtopics = Subtopic.objects.all()
        serializer = SubtopicSerializer(subtopics, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SubtopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def subtopic_detail(request, pk):
    try:
        subtopic = Subtopic.objects.get(pk=pk)
    except Subtopic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubtopicSerializer(subtopic)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SubtopicSerializer(subtopic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        subtopic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# =============================POSTS=================================


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_list_create(request,gradeID,subjectID ):
        user = request.user
        # print("Request data:", request.data)
        # grade_id = request.data.get('grade')
        # subject_id = request.data.get('subject')
        
        try:
            grade = Grade.objects.get(id=gradeID)
            subject = Subject.objects.get(id=subjectID)
        except Grade.DoesNotExist:
            return Response({'error': 'Grade not found'}, status=status.HTTP_404_NOT_FOUND)
        except Subject.DoesNotExist:
            return Response({'error': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(data=request.data)
        Post.objects.create(**request.data, user=user,grade=grade, subject=subject)
        if serializer.is_valid():
            serializer.save(user=request.user, grade=grade, subject=subject)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







@api_view(['GET'])
@permission_classes([AllowAny])
def get_posts_by_grade_and_subject(request, gradeId, subjectId, grade, subject):
    

    try:
        posts = Post.objects.filter(grade=gradeId ,subject=subjectId)
        print("The post works")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Post.DoesNotExist:   
        return Response({'error': 'No posts found'}, status=status.HTTP_404_NOT_FOUND)

# Fetch comments by post
@api_view(['GET'])
@permission_classes([AllowAny])
def get_comments_by_post(request, post_id):
    try:
        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return Response({'error': 'No comments found'}, status=status.HTTP_404_NOT_FOUND)
    
# @api_view(["GET"])
# @permission_classes([AllowAny])
# def posts(request):
#     posts = Post.objects.all()  # complex data
#     serializer = PostSerializer(posts, many=True)
#     return Response(serializer.data)


# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def post_detail_create(request, grade_id, subject_id):
#     user = request.user
#     def get_object():
#         try:
#             grade = Grade.objects.get(pk=grade_id)
#             subject = Subject.objects.get(pk=subject_id)
#             user = request.user
#         except (Grade.DoesNotExist, Subject.DoesNotExist):
#             return None

#         return Post.objects.filter(grade=grade, subject=subject).first()

#     if request.method == 'GET':
#         post = get_object()
#         if not post:
#             return Response(status=404)

#         serializer = PostSerializer(post)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         if not user.is_authenticated:
#             return Response(status=401)

#         try:
#             grade = Grade.objects.get(pk=grade_id)
#             subject = Subject.objects.get(pk=subject_id)
#         except (Grade.DoesNotExist, Subject.DoesNotExist):
#             return Response(status=404)

#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=user, grade=grade, subject=subject)
#             print(user,grade,subject)
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
def post_detail_create(request, grade_id, subject_id):
    try:
        user = request.user
        # grade_id = request.data.get('grade')
        # subject_id = request.data.get('subject')

        grade = Grade.objects.get(id=grade_id)
        subject = Subject.objects.get(id=subject_id)
    except Grade.DoesNotExist or Subject.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        posts = Post.objects.filter(grade=grade, subject=subject)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user,grade=grade, subject=subject)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    







@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_post(request):
    user = request.user

    serializer = PostSerializer(data=request.data)
    Post.objects.create(**request.data, user=user)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
# @permission_classes([IsAuthenticated])
def update_post(request, pk=id):
    post = Post.objects.get(pk=pk)
    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method == "DELETE":
        post.delete()
        return Response("Post deleted successfull")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def likepost(request, pk=id):
    post = Post.objects.get(pk=pk)
    if request.user not in post.likes.all():
        post.likes.add(request.user)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    post.save()
    return Response({"message": "Post liked successfully"})


# ====================================LOGIC============================
@api_view(['POST'])
@permission_classes([IsAuthenticated])

def like_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    post.likes += 1
    post.save()
    return Response({'message': 'Post liked successfully'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def dislike_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    post.dislikes += 1
    post.save()
    return Response({'message': 'Post disliked successfully'})


# =============================COMMENTS=================================


@api_view(["GET"])
@permission_classes([AllowAny])
def comments(request):
    posts = Comment.objects.all()  # complex data
    serializer = CommentSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_comment(request, post_id=id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    data = request.data.copy()
    data['post'] = post.id  # Ensure the post field is included in the data

    serializer = CommentSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=user, post=post)  # Save the comment with the user and post
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)

@api_view(["PUT", "GET", "DELETE"])
@permission_classes([IsAuthenticated])
def update_comment(request, pk=id):
    post = Comment.objects.get(pk=pk)
    if request.method == "GET":
        serializer = CommentSerializer(post)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = CommentSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method == "DELETE":
        post.delete()
        return Response("Comment deleted successfull")


@api_view(['POST'])
@permission_classes([IsAuthenticated])

def like_comment(request, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    comment.likes += 1
    comment.save()
    return Response({'message': 'Comment liked successfully'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def dislike_comment(request, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    comment.dislikes += 1
    comment.save()
    return Response({'message': 'Comment disliked successfully'})

# =============================USERS=================================


@api_view(["GET"])
@permission_classes([AllowAny])
def users(request):
    users = User.objects.all()  # complex data
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["PUT", "GET", "DELETE"])
def update_users(request, pk):
    users = User.objects.get(pk=pk)
    if request.method == "GET":
        serializer = UserSerializer(users)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = UserSerializer(users, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method == "DELETE":
        users.delete()
        return Response("user deleted successfull")

# ======================================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_view(request):
    user_message = request.data.get('message')
    # if user_message:
    #     # response = openai.Completion.create(
    #     #     engine="text-davinci-003",
    #     #     prompt=user_message,
    #     #     max_tokens=150
    #     # )
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": "You are a helpful assistant."},
    #             {"role": "user", "content": user_message},
    #         ]
    #     )
    #     bot_response = response.choices[0].text.strip()
    #     return Response({'response': bot_response})
    return Response({'error': 'No message provided'}, status=400)
# =============================MASSEGES=================================


# @api_view(["GET"])
# def messages():
#     messages = Message.objects.all()  # complex data
#     serializer = MessageSerializer(messages, many=True)
#     return Response(serializer.data)


# @api_view(["POST", "GET"])
# def messages(request, sender=None, receiver=None):
#     # messages = Message.objects.all() #complex data
#     if request.method == "POST":
#         serializer = MessageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#     if request.method == "GET":
#         messages = Message.objects.filter(
#             sender_id=sender, receiver_id=receiver, is_read=False
#         )
#         serializer = MessageSerializer(
#             messages, many=True, context={"request": request}
#         )
#         for message in messages:
#             message.is_read = True
#             message.save()
#         return Response(serializer.data, safe=False)


@api_view(["PUT", "GET", "DELETE"])
def update_messages(request, pk):
    messages = Message.objects.get(pk=pk)
    if request.method == "GET":
        serializer = MessageSerializer(messages)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = MessageSerializer(messages, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method == "DELETE":
        messages.delete()
        return Response("message deleted successfull")


@api_view(['GET'])
def message_list(request):
    """
    List all messages.
    """
    messages = Message.objects.all()
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def message_detail(request, pk):
    """
    Retrieve a single message instance.
    """
    message = Message.objects.get(pk=pk)
    serializer = MessageSerializer(message)
    return Response(serializer.data)

@api_view(['PUT'])
def mark_message_as_read(request, pk):
    """
    Mark a message as read.
    """
    try:
        message = Message.objects.get(pk=pk)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = MessageSerializer(message, data={'is_read': True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def send_message(request):
    """
    Create a new message.
    """
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# =============================NOTIFICATIONS=================================


@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user)
    
    if request.method == "GET":
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    
    if request.method == "DELETE":
        notifications.delete()
        return Response("Notifications deleted successfully")

# @api_view(["GET", "DELETE"])
# @permission_classes([AllowAny])  # You might want to change this to IsAuthenticated
# def notifications_view(request):
#     if request.method == "GET":
#         if request.user.is_authenticated:
#             user_notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
#             serializer = NotificationSerializer(user_notifications, many=True)
#             return Response({'notifications': serializer.data})
#         else:
#             return Response({'error': 'User is not authenticated'}, status=401)
#     elif request.method == "DELETE":
#         Notification.objects.filter(user=request.user).delete()
#         return Response("Notifications deleted successfully")

# =============================================================================================================================================================
from rest_framework import generics, permissions
from .models import Thread
from .serializers import ThreadSerializer
class MessagesPageView(generics.ListAPIView):
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Thread.objects.by_user(user=self.request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from .models import Thread


@login_required
def messages_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads
    }
    print(context)
    return render(request, 'messages.html', context)
