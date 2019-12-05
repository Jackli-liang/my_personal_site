from django.contrib.auth.models import User
from django.db import models
# django-ckeditor
from ckeditor.fields import RichTextField

# Create your models here.
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from article.models import ArticlePost


"""
    评论模型
    1 article---comment  一对多
    2 user------comment  一对多
    3 body------TextField
    4 created---DateTimeField
"""

# 文章的评论
class Comment(MPTTModel):
    article = models.ForeignKey(ArticlePost,verbose_name='评论的文章',
                        on_delete=models.CASCADE,related_name='article_comment')
    user = models.ForeignKey(User,verbose_name='评论的用户',
                        on_delete=models.CASCADE,related_name='user_comment')
    body = RichTextField('评论的内容')
    created = models.DateTimeField('评论的时间',auto_now_add=True)  # 自动添加评论的系统时间

    parent = TreeForeignKey('self',on_delete=models.CASCADE,
                            null=True,blank=True,related_name='children')
    # 记录二级评论回复给谁
    reply_to = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,
                                 related_name='replyers')

    # 替换Meta为MPTTMeta
    class MPTTMeta:
        order_insertion_by = ['created']
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.body[:20]
