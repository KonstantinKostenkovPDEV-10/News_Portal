from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Subscribers, Category
from django.contrib.auth.models import User

from .filters import PostFilter
from .forms import PostForm,SubscribeForm

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from datetime import datetime

from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from .models import Subscribers
from django.core.mail import send_mail

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
    model = Post
    template_name = 'post_create.html'
    permission_required = ('News.add_Post',)
    form_class = PostForm



@method_decorator(login_required(login_url="/sign/login/"), name='dispatch')
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    permission_required = ('News.change_Post',)
    form_class = PostForm
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


@method_decorator(login_required(login_url="/sign/login/"), name='dispatch')
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/post/'
    permission_required = ('News.delete_Post', )

class SubscribersView(LoginRequiredMixin, CreateView):
    template_name = 'subscribers.html'
    form_class = SubscribeForm
    model = Subscribers
    context_object_name = 'subscribers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self,form):

        user = self.request.user
        form.instance.user = User.objects.get(pk=user.id)
        self.object = form.save()
        return redirect('/')
