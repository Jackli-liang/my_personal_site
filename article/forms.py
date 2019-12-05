# 引入表单类
from django import forms
# 引入文章模型
from article.models import ArticlePost

# 写文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = ArticlePost
        # 定义表单包含的字段
        fields = ['title','body','tags','category']

    # def clean(self):
    #     category = self.cleaned_data['category']
    #     if category == '':
    #         raise forms.ValidationError('内容不能为空')

