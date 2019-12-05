from django.contrib import admin

# Register your models here.
from article.models import ArticlePost,Tag,Category

class ArticlePostAdmin(admin.ModelAdmin):
    list_display = ['author','title','created','updated']
    fields = ['title','body','views','tags','category','author']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

# 注册ArticlePost到admin
admin.site.register(ArticlePost,ArticlePostAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Category,CategoryAdmin)



