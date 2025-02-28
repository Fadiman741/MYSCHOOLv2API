from django.urls import path
from .views import (
    get_announcement,
    get_comments_by_post,
    get_posts_by_grade_and_subject,
    post_list_create,
    signup,
    logout_view,
    login_view,
    create_announcement,
    announcement_list,
    update_announcement,
    grade_subject_list,
    grade_list, grade_detail, subject_list, subject_detail, subtopic_list, subtopic_detail,
    post_list_create,
    post_detail_create,
    create_post,
    # posts,
    update_post,
    create_comment,
    comments,
    update_comment,
    users,
    update_users,
    likepost,
    get_notifications,
    like_post, 
    dislike_post, 
    like_comment, 
    dislike_comment, 
    get_current_user,
    update_current_user,
    # notifications_view
    chat_view,
    message_list,
    message_detail,
    mark_message_as_read,
    send_message,
    

)

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("create_announcement/", create_announcement, name="create_announcement"),
    path("announcements/", announcement_list, name="announcement_list"),
    path("update_announcement/<uuid:pk>/", update_announcement, name="update_announcement"),
    path("announcement/<uuid:pk>/", get_announcement, name="get_announcement"),
    # path('grades/', grade_list, name='grade-list'),
    path('grades/', grade_subject_list, name='grade_subject_list'),
    path('grades/<int:pk>/', grade_detail, name='grade-detail'),
    path('subjects/', subject_list, name='subject-list'),
    path('subjects/<int:pk>/', subject_detail, name='subject-detail'),
    path('subtopics/', subtopic_list, name='subtopic-list'),
    path('subtopics/<int:pk>/', subtopic_detail, name='subtopic-detail'),

    # path('posts/<int:grade_id>/<int:subject_id>/', post_list_create, name="post_list_create"),
    # path('posts/<int:grade_id>/<int:subject_id>/', post_detail_create, name="post_detail_create"),
    path("create_post/", create_post, name="create_post"),
    # path("posts/", posts, name="posts"),
    path("post/<uuid:pk>/", update_post, name="update_post"),
    path("posts/<uuid:pk>/like", likepost, name="likepost"),
    path('post/<uuid:post_id>/like/', like_post , name="like_post"),
    path('post/<uuid:post_id>/dislike/', dislike_post),
    path('posts/<uuid:post_id>/comments/', create_comment, name='create_comment'),
    # path("create_comment/", create_comment, name="create_comment"),
    path("comments/", comments, name="comment-list"),
    path("comment/<uuid:pk>/", update_comment, name="comment-detail"),
    path('comment/<uuid:comment_id>/like/', like_comment),
    path('comment/<uuid:comment_id>/dislike/', dislike_comment),
    path("users/", users, name="users"),
    path("update-users/<uuid:pk>/", update_users, name="update_users"),
    path("notifications/", get_notifications, name="get_notifications"),
    # path("notification/", notifications_view, name="notifications_view"),
    path('get_current_user/', get_current_user, name='get_current_user'),
    path('update_current_user   /', update_current_user,name='update_current_user'),
    path('aichat/', chat_view, name='chat'),
    path('messages/', message_list, name='message_list'),
    path('messages/<uuid:pk>/', message_detail, name='message_detail'),
    path('messages/<uuid:pk>/mark-as-read/', mark_message_as_read, name='mark_message_as_read'),
    # New URL for sending a message
    path('messages/send/', send_message, name='send_message'),
    # path('announcements/', views.AnnouncementList.as_view(), name='announcement-list'),

    path('posts/<uuid:gradeId>/<uuid:subjectId>/<slug:grade>/<slug:subject>/', get_posts_by_grade_and_subject, name='get_posts'),
    path('grades/<int:grade_id>/subjects/<int:subject_id>/', post_detail_create, name='post-detail-create'),
    # path('grades/<id:grade_id>/subjects/<id:subject_id>/posts/', post_list_create, name='post_list_create'),
    path('comments/<uuid:post_id>/', get_comments_by_post, name='get_comments'),

    path('create-posts/', post_list_create, name='post-list-create'),

]
# =======================================================================================
