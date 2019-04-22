from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('hashtag/<int:hash_pk>/', views.hashtag, name='hashtag'),
    path('explore/', views.explore, name='explore'),
    path('<int:post_pk>/like/', views.like, name='like'),
    path('<int:post_pk>/comment_delete/<int:comment_pk>/', views.comment_delete, name='comment_delete'),
    path('<int:post_pk>/comment_create/', views.comment_create, name='comment_create'),
    path('<int:post_pk>/delete/', views.delete, name='delete'),
    path('<int:post_pk>/update/', views.update, name='update'),
    path('create/', views.create, name='create'),
    path('', views.list, name='list'),
]