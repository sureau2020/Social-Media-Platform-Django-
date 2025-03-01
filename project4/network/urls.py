
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("<int:user_id>", views.profile, name="profile"),
    path("follow", views.followUnfollow, name="follow"),
    path("following", views.following_view, name="following"),
    path("editAndLike/<int:post_id>", views.editAndLike, name="editAndLike"),
]
