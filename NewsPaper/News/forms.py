from django.forms import ModelForm, BooleanField
from .models import Post



class PostForm(ModelForm):
    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = [
                  'user',
                  'type_post',
                  'title_news',
                  'post',
                  'rating_news',

                  ]