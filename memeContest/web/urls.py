from django.urls import path

from . import views

app_name = "web"
urlpatterns = [
    path('', views.index, name="index"),
    path('post/<int:contest_id>', views.post, name="post"),
    path('details/<int:contest_id>', views.details, name="details"),
]
