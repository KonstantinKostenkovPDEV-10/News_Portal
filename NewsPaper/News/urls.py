from .jobs import job_scheduler
from .views import PostList, PostDetail, PostCreateView, PostUpdateView, PostDeleteView, SubscribersView, AddAuthorView
from django.urls import path


urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('subscribers/', SubscribersView.as_view(),name='subscribers'),
    path('upgrade/',AddAuthorView.as_view(template_name='upgrade.html'),name='upgrade'),
    ]
job_scheduler()