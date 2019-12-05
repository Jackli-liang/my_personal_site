from django.contrib import admin

# Register your models here.
from comment.models import Comment
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','article','body']

admin.site.register(Comment,CommentAdmin)
