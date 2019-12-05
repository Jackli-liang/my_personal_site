from django import template

from article.models import ArticlePost, Category, Tag

register = template.Library()

# 归档的模板标签
@register.inclusion_tag('inclusions/_archives.html',takes_context=True)
def show_archives(context):
    return {
        'date_list': ArticlePost.objects.all().dates('created','month',order='DESC'),
    }



# 最新文章的模板标签
@register.inclusion_tag('inclusions/_new_post.html',takes_context=True)
def show_recent_posts(context,num=3):
    return {
        'recent_post_list': ArticlePost.objects.all().order_by('-created')[:num],
    }

# 分类的模板标签
@register.inclusion_tag('inclusions/_categories.html',takes_context=True)
def show_categories(context):
    return {
        'category_list': Category.objects.all(),
    }

# 标签云的模板标签
@register.inclusion_tag('inclusions/_tags.html',takes_context=True)
def show_tags(context):
    return {
        'tags': Tag.objects.all(),
    }