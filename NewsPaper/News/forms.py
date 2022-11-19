from django.forms import ModelForm, Textarea
from .models import Post,Subscribers,Category, Comment

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_category',
                  'type_post',
                  'title_news',
                  'post',
                  'rating_news',
                  ]
class SubscribeForm(ModelForm):
    class Meta:
        model = Subscribers
        fields = [
                    'category',
                ]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields =[
            'comment_text',
              ]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            self.fields['comment_text'].widget = Textarea(attrs={'rows':3})

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = [
                    'category_name'
                  ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
