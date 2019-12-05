
# 发布评论的表单
from django import forms

from comment.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
