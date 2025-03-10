from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import  User,Announcement,Grade,Subject,AnnouncementLike,AnnouncementComment,AnnouncementCommentLike,AnnouncementReplyLike,AnnouncementReply
from .models import Post, PostComment, PostCommentLike, PostLike, PostReply, PostReplyLike
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff','occupation', 'schoolname', 'profile_picture',
                'years_of_experience', 'role', 'subjects', 
                'school', 'location', 'languages', 
                'facebook', 'twitter', 'linkedin', 'phone')
    search_fields = ('username', 'email', 'first_name', 'last_name','date_joined', 'is_staff','occupation', 'schoolname', 'profile_picture',
                'years_of_experience', 'role', 'subjects', 
                'school', 'location', 'languages', 
                'facebook', 'twitter', 'linkedin', 'phone'  )
    readonly_fields = ('date_joined',)
    fieldsets = (
        ('Personal Info', {'fields': ('username', 'email', 'first_name', 'last_name', 'password')}),
        ('Profile', {'fields': ('occupation', 'schoolname', 'profile_picture', 'years_of_experience', 'role', 'subjects')}),
        ('Contact', {'fields': ('school', 'location', 'languages', 'facebook', 'twitter', 'linkedin', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ('Create User', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )

admin.site.register(User, CustomUserAdmin)

# admin.site.register(Post)

admin.site.register(Grade)
admin.site.register(Subject)

admin.site.register(Announcement)
admin.site.register(AnnouncementLike)

admin.site.register(AnnouncementComment)
# admin.site.register(AnnouncementCommentLike)

admin.site.register(AnnouncementReply)
admin.site.register(AnnouncementReplyLike)

admin.site.register(Post)
admin.site.register(PostLike)

admin.site.register(PostReply)
admin.site.register(PostReplyLike)

admin.site.register(PostComment)
admin.site.register(PostCommentLike)


