from django.urls import path
from django.conf.urls import include, url
from .import views
from .views import (PostView,
                   PostUpdateView,
                   PostDeleteView,
                   PostLikeToggle,
                   PostDetail,
                   PostdetailView,
                   post_like,
                   feedbackView)
app_name = 'posts'
urlpatterns = [
    #path('', views.index, name="home"),
    path('', PostView.as_view(), name="home"),
    path('posts/<str:slug>/update', PostUpdateView.as_view(), name="update_post"),
    path('posts/<str:slug>/delete', PostDeleteView.as_view(), name="delete_post"), 
    #path('posts/<str:slug>/detail', PostDetail.as_view(),name="post_details"),
    path('posts/<str:slug>/detail',PostdetailView.as_view(),name="post_details"),
    path('posts/<str:slug>/like', PostLikeToggle.as_view(), name='like-toggle'),
    #path('posts/<str:slug>/comment', postcomment, name=' Postcomment'),
    path('feedback', feedbackView.as_view(), name='feedback'),
    path('posts/like/', post_like, name='like'),
    path('search/', views.search, name='search'),

]
