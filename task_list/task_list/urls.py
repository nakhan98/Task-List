from django.conf.urls import patterns, url, include
from task_list import views

urlpatterns = patterns("",
    url(r"^/?$", views.task_list, name="task_list"),
    url(r"^register/$", views.register_user, name="register_user"),
    url(r"^login/$", views.login_user, name="login_user"),
    url(r"^logout/$", views.logout_user, name="logout_user"),
    url(r"^about/$", views.about, name="about"),
    url(r"^close_task/(\d+)$", views.close_task, name="close_task"),
    url(r"^add_task/$", views.add_task, name="add_task"),
    url(r"^edit_task/(\d+)$", views.edit_task, name="edit_task"),
    url(r"^delete_task/(\d+)$", views.delete_task, name="delete_task"),
)
