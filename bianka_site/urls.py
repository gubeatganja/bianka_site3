from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostView.as_view(), name='home'),
    path('filter/', views.FilterPostView.as_view(), name='filter'),
    path('search/', views.Search.as_view(), name='search'),
    path('archive/', views.Search.as_view(), name='archive'),
    path('test/', views.test, name='test'),
    path('comment/<int:pk>/', views.AddComment.as_view(), name='add_comment'),
    path('like/', views.AddLike.as_view(), name='add_like'),
    path('post/<slug:post_slug>/', views.PostDetailView.as_view(), name='post_detail'),
    ]