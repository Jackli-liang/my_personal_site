import markdown
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from article.forms import ArticlePostForm
from article.models import ArticlePost, Category, Tag

# 展示所有文章的列表
# 且有分页功能
from comment.forms import CommentForm
from comment.models import Comment

"""
 对于文章列表,我们要实现两种方式
 1  默认按文章的创建时间排序,这个我们在创建文章的model时
    指定了内部类的ordering = ['-created'],即从库里查询的文章都是按时间排好的
 2  建立一个按钮,点击最热时,按浏览量来排序文章,在文章的列表复用代码
 总结:建立判断语句,判断查询语句中的条件返回文章列表
"""
def article_list(request):
    search = request.GET.get('search','')
    order = request.GET.get('order','')
    comment_form = CommentForm()
    # 对搜索之后的文章的展示
    if search:
        if order == 'views':
            # 搜索之后用浏览量排序
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) | Q(body__icontains=search)
            ).order_by('-views')
        else:
            # 默认的按创建时间排序
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) | Q(body__icontains=search)
            )
    else:
        # 将search参数重置为空
        search = ''

        # 搜索之前的文章的展示
        if order == 'views':
            article_list = ArticlePost.objects.all().order_by('-views')
        else:
            article_list = ArticlePost.objects.all()

    page_size = 5  # 一页显示5篇文章
    # 从页面获取当前页的页码,如果没有,默认为1
    now_page = int(request.GET.get('page',1))
    # 对article_list进行分页操作
    p = Paginator(article_list,page_size)
    # 对当前页进行处理
    articles = p.page(now_page)
    return render(request,'article/list.html',{
        'articles':articles,
        'order':order,
        'search':search,
        'comment_form':comment_form,

    })


# 查询文章的详情
# 浏览文章加1
def article_detail(request,pk):
    article = get_object_or_404(ArticlePost,pk=pk)
    # 取出文章评论,通过网址的参数及article的id找到article
    comments = Comment.objects.filter(article=pk)
    # 在前台使用评论表单
    comment_form = CommentForm()
    # 浏览量 +1
    article.views = F('views') + 1
    # 指定只对浏览量保存
    article.save(update_fields=['views'])
    # 强制刷新数据库，从数据库取数据
    article.refresh_from_db()
    # 将markdown语法渲染成html样式
    md = markdown.Markdown(
                   extensions=[
                       # 包含 缩写、表格等常用扩展
                       'markdown.extensions.extra',
                       # 语法高亮扩展
                       'markdown.extensions.codehilite',
                       # 目录拓展
                       'markdown.extensions.toc',
                   ])
    article.body  = md.convert(article.body)
    return render(request,'article/detail.html',{
        'article':article,
        'toc':md.toc,
        'comments':comments,
        'comment_form':comment_form,
    })

# 写文章的视图
def article_create(request):
    # 判断提交方式
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST)
        # 验证表单是否合法
        if article_post_form.is_valid():
            # 合法,保存数据但不保存到数据库
            # 得到实例的具体对象----文章
            new_article = article_post_form.save(commit=False)
            # 指定文章的作者
            new_article.author = User.objects.get(pk=request.user.pk)

            # 将新文章保存到数据库
            new_article.save()
            # 发表完文章,重定向到文章列表
            return redirect('article:article_list')
        # 如果表单数据不合法
        else:
            return HttpResponse('表单内容有误,请重新填写')

    # GET请求
    else:
        article_post_form = ArticlePostForm()
    return render(request,'article/create.html',{
        'article_post_form':article_post_form,
    })

# 安全删除文章的视图
def article_safe_delete(request,pk):
    # pk为你点击的哪一篇文章
    # user = User.objects.get(is_superuser=1)
    article=get_object_or_404(ArticlePost, pk=pk)
    if request.method == 'POST':
        if request.user != article.author:
            return HttpResponse("抱歉,你没有权限删除文章。")

        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse('仅允许提交post请求')

# 需求:我们可能觉得第一次写的内容有错误.需要修改
# 修改文章的视图
def article_update(request,pk):
    """
    通过POST方法提交表单,更改title,body字段内容
    通过GET方法进入初始表单页面
    :param request: POST,GET
    :param pk: article.pk
    :return: 修改后的文字详情页
    """
    # user=User.objects.get(is_superuser=1)
    article = get_object_or_404(ArticlePost, pk=pk)
    if request.method == 'POST':
        if request.user != article.author:
            return HttpResponse("你没有权限修改文章。")
        # 得到提交数据的表单实例
        article_post_form = ArticlePostForm(request.POST)

        # 验证是否合法
        if article_post_form.is_valid():
            # 合法,则把修改的内容得到
            article.title = article_post_form.cleaned_data['title']
            article.body = article_post_form.cleaned_data['body']
            article.tags = article_post_form.cleaned_data['tags']
            article.category = article_post_form.cleaned_data['category']

            article.save()
            # 完成修改后回到修改后的文章
            return redirect('article:article_detail',pk=pk)
        # 不合法
        else:
            return HttpResponse('表单内容有误,请重新填写')
    # GET请求获取数据
    else:
        article_post_form = ArticlePostForm()
        return render(request,'article/update.html',{
            'article':article,
            'article_post_form':article_post_form,
        })


# 归档页面
def archives(request,year,month):
    post_list = ArticlePost.objects.filter(created__year = year,
                                            created__month = month).order_by('-created')
    return render(request,'article/list.html',{
        'articles':post_list,
    })


# 分类页面
def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = ArticlePost.objects.filter(category=cate).order_by('-created')
    return render(request,'article/list.html',{
        'articles':post_list,
    })

# 标签页面
def tag(request,pk):
    t = get_object_or_404(Tag,pk=pk)
    post_list = ArticlePost.objects.filter(tags=t).order_by('-created')

    return render(request,'article/list.html',{
        'articles':post_list,
    })

