import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import ( api_view,permission_classes, authentication_classes)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authtoken.models import Token
# ====  USER & GRADES  ======================================================================================================
from users.models import User, Grade, Subject, Subtopic
from .serializers import ( UserSerializer,GradeSerializer, SubjectSerializer)
# ====  ANNOUCEMENTS  =======================================================================================================
from .models import Announcement, AnnouncementLike, AnnouncementComment, AnnouncementCommentLike, AnnouncementReply, AnnouncementReplyLike
from .serializers import AnnouncementSerializer, AnnouncementLikeSerializer, AnnouncementCommentSerializer, AnnouncementCommentLikeSerializer, AnnouncementReplySerializer, AnnouncementReplyLikeSerializer
# ====  POSTS  ==============================================================================================================

from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import TokenAuthentication

# ====   UTHENTICATION  =====================================================================================================
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


# ====  MENU DROP-DOWN  =================================================================================================================

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

# ====  ANNOUNCEMENT  ==================================================================================================

@api_view(["GET"])
@permission_classes([AllowAny])
def announcement_list(request):
    announcement = Announcement.objects.all()  # complex data
    serializer = AnnouncementSerializer(announcement, many=True)
    return Response(serializer.data)

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_announcement(request):
    user = request.user  # Assuming you are using authentication
    serializer = AnnouncementSerializer(data=request.data)
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
        serializer = AnnouncementSerializer(announcement)
        return Response(serializer.data)
    
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
def update_announcement(request, pk=id):
    announcement = Announcement.objects.get(pk=pk)
    if request.method == "GET":
        serializer = AnnouncementSerializer(announcement)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = AnnouncementSerializer(announcement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method == "DELETE":
        announcement.delete()
        return Response("Announcement deleted successfull")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_announcement(request, announcement_id):
    try:
        announcement = Announcement.objects.get(id=announcement_id)
    except Announcement.DoesNotExist:
        return Response({"error": "Announcement not found"}, status=status.HTTP_404_NOT_FOUND)

    like, created = AnnouncementLike.objects.get_or_create(user=request.user, announcement=announcement)
    if not created:
        like.delete()
        return Response({"status": "unliked"}, status=status.HTTP_200_OK)
    return Response({"status": "liked"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, announcement_id):
    try:
        announcement = Announcement.objects.get(id=announcement_id)
    except Announcement.DoesNotExist:
        return Response({"error": "Announcement not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AnnouncementCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, announcement=announcement)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_announcement_reply(request, comment_id):
    comment = get_object_or_404(AnnouncementComment, id=comment_id)
    user = request.user
    content = request.data.get('content')

    if not content:
        return Response({'status': 'error', 'message': 'Content is required.'}, status=status.HTTP_400_BAD_REQUEST)

    reply = AnnouncementReply.objects.create(
        user=user,
        comment=comment,
        content=content
    )

    return Response({
        'status': 'success',
        'message': 'Reply added successfully.',
        'reply_id': reply.id,
        'content': reply.content,
        'created_at': reply.created_at
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_announcement_reply(request, reply_id):
    reply = get_object_or_404(AnnouncementReply, id=reply_id)
    user = request.user

    like, created = AnnouncementReplyLike.objects.get_or_create(user=user, reply=reply)

    if not created:
        like.delete()
        message = "Reply unliked successfully."
    else:
        message = "Reply liked successfully."

    return Response({
        'status': 'success',
        'message': message,
        'like_count': reply.like_count
    }, status=status.HTTP_200_OK)

# =============================POSTS=================================

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def post_list_create(request,gradeID,subjectID ):
#         user = request.user
#         # print("Request data:", request.data)
#         # grade_id = request.data.get('grade')
#         # subject_id = request.data.get('subject')
        
#         try:
#             grade = Grade.objects.get(id=gradeID)
#             subject = Subject.objects.get(id=subjectID)
#         except Grade.DoesNotExist:
#             return Response({'error': 'Grade not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Subject.DoesNotExist:
#             return Response({'error': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = PostSerializer(data=request.data)
#         Post.objects.create(**request.data, user=user,grade=grade, subject=subject)
#         if serializer.is_valid():
#             serializer.save(user=request.user, grade=grade, subject=subject)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_posts_by_grade_and_subject(request, gradeId, subjectId, grade, subject):
    

#     try:
#         posts = Post.objects.filter(grade=gradeId ,subject=subjectId)
#         print("The post works")
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Post.DoesNotExist:   
#         return Response({'error': 'No posts found'}, status=status.HTTP_404_NOT_FOUND)

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# # @permission_classes([AllowAny])
# def post_detail_create(request, grade_id, subject_id):
#     try:
#         user = request.user
#         # grade_id = request.data.get('grade')
#         # subject_id = request.data.get('subject')

#         grade = Grade.objects.get(id=grade_id)
#         subject = Subject.objects.get(id=subject_id)
#     except Grade.DoesNotExist or Subject.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         posts = Post.objects.filter(grade=grade, subject=subject)
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=user,grade=grade, subject=subject)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    







# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def create_post(request):
#     user = request.user

#     serializer = PostSerializer(data=request.data)
#     Post.objects.create(**request.data, user=user)
#     if serializer.is_valid():
#         serializer.save(user=user)
#         return Response(serializer.data)
#     else:
#         return Response(serializer.errors)


# @api_view(["GET", "PUT", "DELETE"])
# @permission_classes([AllowAny])
# # @permission_classes([IsAuthenticated])
# def update_post(request, pk=id):
#     post = Post.objects.get(pk=pk)
#     if request.method == "GET":
#         serializer = PostSerializer(post)
#         return Response(serializer.data)

#     if request.method == "PUT":
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)

#     if request.method == "DELETE":
#         post.delete()
#         return Response("Post deleted successfull")


# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def likepost(request, pk=id):
#     post = Post.objects.get(pk=pk)
#     if request.user not in post.likes.all():
#         post.likes.add(request.user)
#     if request.user in post.dislikes.all():
#         post.dislikes.remove(request.user)
#     post.save()
#     return Response({"message": "Post liked successfully"})


# # ====================================LOGIC============================
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])

# def like_post(request, post_id):
#     try:
#         post = Post.objects.get(pk=post_id)
#     except Post.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     post.likes += 1
#     post.save()
#     return Response({'message': 'Post liked successfully'})

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])

# def dislike_post(request, post_id):
#     try:
#         post = Post.objects.get(pk=post_id)
#     except Post.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     post.dislikes += 1
#     post.save()
#     return Response({'message': 'Post disliked successfully'})

# # =============================COMMENTS=================================

# # =============================USERS=================================


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
