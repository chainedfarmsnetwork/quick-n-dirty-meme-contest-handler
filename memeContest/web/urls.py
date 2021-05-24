from django.urls import path

from . import views

app_name = "web"
urlpatterns = [
    path('', views.index, name="index"),
    path('details/<int:contest_id>', views.details, name="details"),
    path('post_contest/<int:contest_id>',
         views.post_contest, name="post_contest"),
    path('post_retweet/<int:contest_id>',
         views.post_retweet, name="post_retweet"),
]
