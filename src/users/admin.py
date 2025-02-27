from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Post,Announcement,Comment,Grade,Subject,Thread,ChatMessage,ThreadManager

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

admin.site.register(User, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Announcement)
admin.site.register(Comment)
admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Thread)
admin.site.register(ChatMessage)
# admin.site.register(ThreadManager)


