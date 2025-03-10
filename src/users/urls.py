from django.urls import path
# ==== USER ===========================
from .views import ( grade_subject_list, like_comment, like_reply, post_detail_create, post_list_create, signup,logout_view,login_view,get_current_user, update_post,users,update_users,update_current_user,
    # ,
    # announcement_list,
    # ,
    # add_announcement_reply,
    # like_announcement_reply,
    # ,
    # get_comments_by_post,
    # get_posts_by_grade_and_subject,
    # post_list_create,


    # like_announcement, add_comment, add_reply,
    # grade_subject_list,
    # 
    # post_list_create,
    # post_detail_create,
    # create_post,
    # # posts,
    # update_post,
    # create_comment,
    # comments,
    # update_comment,

)
# ==== MENU DROPDOWN ======
from .views import (grade_list, grade_detail, subject_list, subject_detail);
# ==== ANNOUCEMENTS =====================
from .views import announcement_list,create_announcement,get_announcement,update_announcement,like_announcement,add_announcement_comment, like_announcement_coment
# ==== POSTS ========================
from .views import get_posts_by_grade_and_subject
# add_announcement_reply,like_announcement_reply, 

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
    path('announcements/<uuid:announcement_id>/like/', like_announcement, name='like-announcement'),
    path('announcements/<uuid:announcement_id>/comment/', add_announcement_comment, name='add-announcement-comment'),
    path('announcement-comments/<uuid:announcement_comment_id>/like/', like_announcement_coment, name='like-announcement-comment'),

    # =====  POSTS  =====
    path('posts/<int:gradeId>/<int:subjectId>/<str:grade>/<str:subject>/', get_posts_by_grade_and_subject, name='get_posts_by_grade_and_subject'),
    path('comments/<uuid:comment_id>/like/', like_comment, name='like_comment'),
    path('replies/<uuid:reply_id>/like/', like_reply, name='like_reply'),
    path("post/<uuid:pk>/", update_post, name="update_post"),
    # path("posts/<uuid:pk>/like", likepost, name="likepost"),
    # path('post/<uuid:post_id>/like/', like_post , name="like_post"),
    # path('post/<uuid:post_id>/dislike/', dislike_post),
    # path('posts/<uuid:post_id>/comments/', create_comment, name='create_comment'),
    
























































































    # # ====  POSTS  =====

    # # path("create_comment/", create_comment, name="create_comment"),
    # path("comments/", comments, name="comment-list"),
    # path("comment/<uuid:pk>/", update_comment, name="comment-detail"),
    # path('comment/<uuid:comment_id>/like/', like_comment),
    # path('comment/<uuid:comment_id>/dislike/', dislike_comment),






    # path('grades/', grade_list, name='grade-list'),

 

    # path('posts/<int:grade_id>/<int:subject_id>/', post_list_create, name="post_list_create"),
    # path('posts/<int:grade_id>/<int:subject_id>/', post_detail_create, name="post_detail_create"),
    # path("create_post/", create_post, name="create_post"),
   
    # path("notifications/", get_notifications, name="get_notifications"),
    # # path("notification/", notifications_view, name="notifications_view"),
    # path('aichat/', chat_view, name='chat'),
    

    # path('grades/<int:grade_id>/subjects/<int:subject_id>/', post_detail_create, name='post-detail-create'),
    # # path('grades/<id:grade_id>/subjects/<id:subject_id>/posts/', post_list_create, name='post_list_create'),
    # path('comments/<uuid:post_id>/', get_comments_by_post, name='get_comments'),

    # path('create-posts/', post_list_create, name='post-list-create'),

]
# =======================================================================================
