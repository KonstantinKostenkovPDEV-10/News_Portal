from django.urls import path
from .views import PostList, PostDetail, PostCreateView, PostUpdateView, PostDeleteView, SubscribersView

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('subscribers/', SubscribersView.as_view(),name='Subscribers'),

]
