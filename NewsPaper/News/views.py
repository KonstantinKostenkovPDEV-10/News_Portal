from django.contrib import messages
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormMixin
from .models import Post, Subscribers, Category,PostCategory,Comment
from django.contrib.auth.models import User
from .signals import limit_post
from django.contrib.auth.models import Group,UserManager
from .filters import PostFilter
from .forms import PostForm,SubscribeForm,CommentForm,CategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, redirect
from .models import Subscribers,Author



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

class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False
    def form_valid(self, form):
        messages.success(self.request,self.success_msg)
        return super().form_valid(form)
    def get_success_url(self):
        return '%s?id=%s' % (self.success_url,self.object().id)

class PostDetail(CustomSuccessMessageMixin,FormMixin,DetailView):
    template_name = 'post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm
    queryset = Post.objects.all()
    success_msg = 'Коментарий успешно добавлен!'
    success_url = '/post/'

    def get_success_url(self,**kwargs):
        return reverse('post_detail',kwargs={'pk':self.get_object().id})

    def form_valid(self,form):

        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def post(self,request,*args,**kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

@method_decorator(login_required(login_url="/sign/login/"), name='dispatch')
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    model = Post
    template_name = 'post_create.html'
    permission_required= ('News.add_post',)
    form_class = PostForm

    def get(self,request):
        cat=Category.objects.all()
        bound_form=self.get_form()
        return render(request,'post_create.html',context={'form':bound_form,'cat':cat})

    def post(self, request, *args, **kwargs,):
        username = request.user
        New_Post = Post(author_id=Author.objects.filter(user_id=User.objects.filter(username=username).first().id).values('id'),
                         type_post=request.POST.get('type_post'),
                         title_news=request.POST.get('title_news'),
                         post=request.POST.get('post'),
                        )
        New_Post.save(request.POST)
        New_Post_Category = request.POST.get('post_category')
        New_Post.post_category.add(New_Post_Category)

        return redirect('/')



@method_decorator(login_required(login_url="/sign/login/"), name='dispatch')
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    permission_required = ('News.change_post',)
    form_class = PostForm
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


@method_decorator(login_required(login_url="/sign/login/"), name='dispatch')
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/post/'
    permission_required = ('News.delete_post', )


@method_decorator(login_required(login_url="/sign/login/"), name='dispatch')
class AddAuthorView(LoginRequiredMixin,TemplateView):
    model = Author
    template_name = 'upgrade.html'

    def get(self, request):
        if not request.user.groups.filter(name='authors').exists():
            user_status = 1
        else:
            user_status = 0
        return render(request, 'upgrade.html', {'user_status': user_status})

    def post(self,request):
        username = request.user
        authors_group = Group.objects.get(name='authors')

        if not request.user.groups.filter(name='authors').exists():
            NewAuthor = Author(user=username)
            NewAuthor.save()
            user_status = 0
            authors_group.user_set.add(User.objects.filter(username=username).first().id)
        else:
            user_status = 1
        return render(request, 'upgrade.html', {'user_status': user_status})


@method_decorator(login_required(login_url="/sign/login/"), name='dispatch')
class SubscribersView(LoginRequiredMixin, CreateView):
    template_name = 'subscribers.html'
    form_class = SubscribeForm
    model = Subscribers
    context_object_name = 'subscribers'

    def get(self, request):
        cat = Category.objects.all()
        bound_form = self.get_form()
        return render(request, 'subscribers.html', context={'form': bound_form, 'cat': cat})

    def form_valid(self, form):
        self.object = form.save()
        self.object.subscribers = self.get_object()
        self.object.save()
        return super().form_valid(form)

    def post(self,request, *args, **kwargs):
        username = request.user
        subs = Subscribers(user_id=User.objects.filter(username=username).first().id,
                           category_id=request.POST.get('category'))
        subs.save()
        bound_form = self.get_form()
        #q_list=Subscribers.objects.filter(user_id=User.objects.filter(username=username).first().id).values('category_id')
        Sub=Category.objects.filter(id=request.POST.get('category'))
        #Sub = Category.objects.filter(id=q_list)
        Subscribers_user=Sub.get()

        return render(request, 'subscribers_user.html',context={'form': bound_form,'Subscribers_user':Subscribers_user})

