from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="poster")
    content = models.TextField(blank=False)
    like = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(default=False)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True,related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="like_user")


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True,related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="commentor")
    comment = models.TextField(blank=True)
    time = models.DateTimeField(auto_now_add=True)

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="befollowd")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="followings")
    time = models.DateTimeField(auto_now_add=True)


class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="owner")
    following = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="followers")
    time = models.DateTimeField(auto_now_add=True)