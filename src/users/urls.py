from django.urls import path

from .views import (
    get_announcement,
    get_comments_by_post,
    get_posts_by_grade_and_subject,
    post_list_create,
    signup,
    logout_view,
    login_view,
    get_current_user,
    create_announcement,
    announcement_list,
    update_announcement,
    add_announcement_reply,
    like_announcement_reply,



    like_announcement, add_comment, add_reply,
    grade_subject_list,
    grade_list, grade_detail, subject_list, subject_detail,
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
    like_post, 
    dislike_post, 
    
    update_current_user,

)
from .views import announcement_list, announcement_detail, like_announcement, comment_announcement, like_comment, reply_comment, like_reply

urlpatterns = [

    # ===== USER =====
    path("signup/", signup, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('get_current_user/', get_current_user, name='get_current_user'),
    path("users/", users, name="users"),
    path('update_current_user   /', update_current_user,name='update_current_user'),
    path("update-users/<uuid:pk>/", update_users, name="update_users"),



    # =====  MENU =====
    path('grades/', grade_subject_list, name='grade_subject_list'),
    path('grades/<int:pk>/', grade_detail, name='grade-detail'),
    path('subjects/', subject_list, name='subject-list'),
    path('subjects/<int:pk>/', subject_detail, name='subject-detail'),

    # =====  ANNOUNCEMENTS  =====
    path("create_announcement/", create_announcement, name="create_announcement"),
    path("announcements/", announcement_list, name="announcement_list"),
    path("update_announcement/<uuid:pk>/", update_announcement, name="update_announcement"),
    path("announcement/<uuid:pk>/", get_announcement, name="get_announcement"),
    path('announcements/like/', like_announcement, name='like-announcement'),
    path('announcements/comment/', comment_announcement, name='comment-announcement'),
    path('comments/like/', like_comment, name='like-comment'),
    path('comments/reply/', reply_comment, name='reply-comment'),
    path('replies/like/', like_reply, name='like-reply'),

    # # ====  POSTS  =====
    # path("post/<uuid:pk>/", update_post, name="update_post"),
    # path("posts/<uuid:pk>/like", likepost, name="likepost"),
    # path('post/<uuid:post_id>/like/', like_post , name="like_post"),
    # path('post/<uuid:post_id>/dislike/', dislike_post),
    # path('posts/<uuid:post_id>/comments/', create_comment, name='create_comment'),
    # # path("create_comment/", create_comment, name="create_comment"),
    # path("comments/", comments, name="comment-list"),
    # path("comment/<uuid:pk>/", update_comment, name="comment-detail"),
    # path('comment/<uuid:comment_id>/like/', like_comment),
    # path('comment/<uuid:comment_id>/dislike/', dislike_comment),






    # Add a reply to an announcement comment
    path('announcement-comments/<uuid:comment_id>/replies/add/', add_announcement_reply, name='add_announcement_reply'),
    # Like an announcement reply
    path('announcement-replies/<uuid:reply_id>/like/', like_announcement_reply, name='like_announcement_reply'),
    # path('grades/', grade_list, name='grade-list'),

 

    # path('posts/<int:grade_id>/<int:subject_id>/', post_list_create, name="post_list_create"),
    # path('posts/<int:grade_id>/<int:subject_id>/', post_detail_create, name="post_detail_create"),
    path("create_post/", create_post, name="create_post"),
   
    path("notifications/", get_notifications, name="get_notifications"),
    # path("notification/", notifications_view, name="notifications_view"),
    path('aichat/', chat_view, name='chat'),
    

    path('grades/<int:grade_id>/subjects/<int:subject_id>/', post_detail_create, name='post-detail-create'),
    # path('grades/<id:grade_id>/subjects/<id:subject_id>/posts/', post_list_create, name='post_list_create'),
    path('comments/<uuid:post_id>/', get_comments_by_post, name='get_comments'),

    path('create-posts/', post_list_create, name='post-list-create'),

]
# =======================================================================================
