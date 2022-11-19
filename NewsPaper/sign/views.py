from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.contrib.auth.views import TemplateView

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, reverse, redirect



class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/news/'

    def post(self, request):
        user_data = User(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password1'],
        )
        User.objects.create_user(username=user_data.username,
                                        password=user_data.password,
                                        first_name=user_data.first_name,
                                        last_name=user_data.last_name,
                                        email=user_data.email,
                                        is_staff=True )
        user = user_data.username
        email = user_data.email
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(User.objects.filter(username=user).first().id)
        msg = EmailMultiAlternatives \
                (
                subject =f'"Здравствуйте, поздравляем с регистрацией!" {user}',
                body =f"Добро пожаловать на новостной портал News_portal, {user}",
                from_email ='admin008@mail.ru',
                to =[email],
                )

        html_content = render_to_string(
            'send_created.html',
            {
                'user_data': user_data,
            }
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return redirect('/')



