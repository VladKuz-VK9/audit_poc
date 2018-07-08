from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.PostList.as_view(), name='all'),
    path('new/', views.CreatePost.as_view(), name='create'),
    path('by/<username>/', views.UserPost.as_view(), name='for_user'),
    path('by/<username>/<pk:int>', views.PostDetail.as_view(), name='single'),
    path('delete/<pk:int>/', views.DeletePost.as_view(), name='delete'),
]