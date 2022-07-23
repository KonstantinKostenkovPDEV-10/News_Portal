
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('News.urls')),
    path('admin/', admin.site.urls),
    path('news/', include('News.urls')),
    path('post/', include('News.urls')),
    path('accounts/', include('allauth.urls')),
    path('sign/', include('sign.urls')),
    ]