from PIL import Image
from django.db import models


# Create your models here.
from django.contrib.auth.models import User, AbstractUser
# timezone 用于处理时间相关事务。
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    name = models.CharField('分类名',max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField('标签名',max_length=100)

    class Meta:
       verbose_name = '标签'
       verbose_name_plural = verbose_name

    def __str__(self):
       return self.name

# 博客文章数据模型
class ArticlePost(models.Model):

    author = models.ForeignKey(User,verbose_name='文章作者', on_delete=models.CASCADE)

    title = models.CharField('文章标题',max_length=100)
    body = models.TextField('文章正文')
    created = models.DateTimeField('创建时间',auto_now_add=True)
    updated = models.DateTimeField('更新时间',auto_now=True)
    views = models.PositiveIntegerField('浏览量',default=0)
    # 文章与分类的关系 一个分类下面可以有多篇文章
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE,null=True,blank=True)
    # 文章有标签的关系  多对多
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True,related_query_name='article_tag')


    class Meta:
        ordering = ['-created']
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    # 获取文章的地址
    def get_absolute_url(self):
        return reverse('article:article_detail',kwargs={'pk':self.pk})



