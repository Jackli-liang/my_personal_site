from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# 引入内置信号
from django.db.models.signals import post_save
# 引入信号接收器的装饰器
from django.dispatch import receiver

"""
    用户管理这块,我们不满足User的内置模型,字段太少
    电话号码,头像都没有,我们需要对它进行拓展
"""

# 用户拓展信息
class Profile(models.Model):
    # 与User 模型构成一对一的关系
    user = models.OneToOneField(User,verbose_name='用户名称',on_delete=models.CASCADE,related_name='profile')
    phone = models.CharField('电话号码',max_length=20,blank=True)
    avatar = models.ImageField('用户头像',upload_to='avatar/%Y%m%d',blank=True)
    desc = models.TextField('用户简介',max_length=500,blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)

# 每当创建一个admin后台管理员时,便会创建一个用户
# 信号接收函数,每当新建User实例时自动调用
# @receiver(post_save,sender=User)
# def create_user_profile(sender,instance,created,**kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# 信号接收函数,每当更新User实例时自动调用
# @receiver(post_save,sender=User)
# def save_user_profile(sender,instance,**kwargs):
#     instance.profile.save()
# 通过信号的传递，实现了每当User创建/更新时，Profile也会自动的创建/更新。