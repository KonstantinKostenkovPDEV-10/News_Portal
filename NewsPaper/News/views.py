from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import Post

from .filters import PostFilter
from .forms import PostForm

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class PostList(ListView):
    model = Post
    ordering = 'date_time_create'
    template_name = 'post_list.html'
    context_object_name = 'post'
    paginate_by = 1
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

@method_decorator(login_required(login_url="/sign/login/"), name='dispatch')
class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'post_create.html'
    permission_required = ('News.add_Post',)
    form_class = PostForm


# дженерик для редактирования объекта
@method_decorator(login_required(login_url="/sign/login/"), name='dispatch')
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    permission_required = ('News.change_Post',)
    form_class = PostForm
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

# дженерик для удаления товара
@method_decorator(login_required(login_url="/sign/login/"), name='dispatch')
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/post/'
    permission_required = ('News.delete_Post', )


