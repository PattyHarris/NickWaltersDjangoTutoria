from django.conf.urls import url
from . import views

app_name = 'posts'

urlpatterns = [
    url(r'^create/', views.create, name='create'),
    url(r'^(?P<primaryKey>[0-9]+)/upvote', views.upvote, name='upvote'),
    url(r'^(?P<primaryKey>[0-9]+)/downvote', views.downvote, name='downvote'),
    url(r'^(?P<postAuthor>[\w.@+-]+)/$', views.user_posts, name='user_posts'),

]
