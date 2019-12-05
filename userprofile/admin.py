from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from django.contrib.auth.models import User

from userprofile.models import Profile

"""
 在后台当中,我们希望把User,Profile合并为一张表展示
"""
# 定义一个行内admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = '用户信息'

# 将Profile关联到User中
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]

# 注册
admin.site.unregister(User)
admin.site.register(User,UserAdmin)