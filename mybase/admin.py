from django.contrib import admin
from mybase.models import Topic, Page, UserProfile, Comment, PostLike, PostHistory, TopicHistory

class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic')

admin.site.register(Topic, TopicAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(PostLike)

admin.site.register(PostHistory)
admin.site.register(TopicHistory)