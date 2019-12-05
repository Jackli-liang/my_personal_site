from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

# Create your views here.
from userprofile.forms import UserLoginForm, UserRegisterForm, ProfileForm
from userprofile.models import Profile


# class LoginView(View):
#     pass

# 用户登录视图
def user_login(request):
    # 用户第二次登录POST请求
    if request.method == 'POST':
        # 从前端的表单的提交数据获取用户登录信息
        user_login_form = UserLoginForm(data=request.POST)
        # 验证是否合法
        if user_login_form.is_valid():
            # 合法,cleaned_data清洗数据
            data = user_login_form.cleaned_data
            # 检验账号,密码是否正确匹配数据库中的用户
            # 匹配的到,则返回这个user对象
            user = authenticate(username=data['username'],password=data['password'])
            if user:
                # 将用户数据保存在session中,实现登录动作
                login(request,user)
                # 登录成功,返回文章列表
                return redirect('article:article_list')
            else:
                # return HttpResponse('账号或密码输入有误,请重新输入')
                return render(request,'userprofile/login.html',{'msg':'用户名或密码不正确'})
        else:
            return render(request,'userprofile/login.html',{'user_login_form':user_login_form})


    # 用户第一次登录,我们需要把登录界面呈现给用户来登录
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        return render(request,'userprofile/login.html',{
            'form':user_login_form,
        })
    else:
        return HttpResponse('请使用GET或POST请求数据')


# 用户退出的视图
def user_logout(request):
    logout(request)
    # 退出登录后回到文章列表
    return redirect('article:article_list')

# 用户注册的视图
def user_register(request):
    if request.method == 'POST':
        # 得到用户提交数据的注册表单的实例
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            # 合法
            new_user = user_register_form.save(commit=False)
            # 把表单中输入的密码作为用户密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 注册成功之后返回到文章列表
            return redirect('article:article_list')
        else:
            # 不合法
            return HttpResponse('注册表单输入有误,请重新输入')
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        return render(request,'userprofile/register.html',{
            'form':user_register_form
        })
    else:
        return HttpResponse('请使用GET或POST请求提交数据')

# 用户删除自己的账号
# 装饰器要求,用户必须登录,才能删除账号
# 如果未登录,就将页面重定向到/userprofile/login/
@login_required(login_url='/userprofile/login/')
def user_delete(request,pk):
    if request.method == 'POST':
        user = get_object_or_404(User,pk=pk)
        # 验证登录用户,待删除的用户是否相同
        if request.user  == user:
            # 退出登录,删除数据并返回博客文章列表
            logout(request)
            user.delete()
            return redirect('article:article_list')
    else:
        return HttpResponse('仅接受POST请求')

# 编辑用户信息视图
@login_required(login_url='/userprofile/login/')
def profile_edit(request,pk):
    user = get_object_or_404(User,pk=pk)
    # user_id是一对一生成的关联字段
    if Profile.objects.filter(user_id=pk).exists():
        profile = Profile.objects.get(user_id=pk)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        # 验证修改数据者,是否为本人
        if request.user != user:
            return HttpResponse('您没有权限修改此用户的信息')
        # 本人,取到前端提交的编辑后的用户信息
        profile_form = ProfileForm(request.POST,request.FILES)
        # 验证提交的信息是否合法
        if profile_form.is_valid():
            # 合法
            profile_list = profile_form.cleaned_data
            profile.phone = profile_list['phone']
            profile.desc = profile_list['desc']
            # 如果request.FIELS存在文件,则保存
            if 'avatar' in request.FILES:
                profile.avatar = profile_list['avatar']

            profile.save()

            # 保存到数据库后,重定向到编辑页面
            return redirect('userprofile:edit',pk=pk)
        else:
            # 不合法
            return HttpResponse('注册表单输入有误,请重新输入')
    elif request.method == 'GET':
        return render(request,'userprofile/edit.html',{
            'profile':profile,
            'user':user,
        })
    else:
        return HttpResponse('请使用GET或POST请求数据')
