import markdown
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from comment.models import Comment
from article.models import ArticlePost
from comment.forms import CommentForm

# 文章评论的视图函数
@login_required(login_url='/userprofile/login/')
def post_comment(request,article_id,parent_comment_id=None):
    article = get_object_or_404(ArticlePost,id=article_id)

    # 处理POST请求
    if request.method == 'POST':
        # 从提交的数据里面拿到CommentForm的实例,生成一个绑定用户提交评论的表单
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                print(parent_comment)
                # 若回复层级超过二级,则转换为二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user

                new_comment.save()
                return HttpResponse('200 OK')

            new_comment.save()
            # 此处的实现方法有多种
            return redirect(article)
        else:
            return HttpResponse('表单内容有误,请重新填写')
    # 处理GET请求
    elif request.method == 'GET':
        comment_form = CommentForm()
        return render(request,'comment/reply.html',{
            'comment_form':comment_form,
            'article_id':article_id,
            'parent_comment_id':parent_comment_id,
        })
    else:
        return HttpResponse('仅接受GET/POST请求')
