from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from operator import attrgetter
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse



from .models import User,Post,Like, Follower, Following  


def index(request):
    posts = Post.objects.all().order_by('-created_at')
    if request.user.is_authenticated:
        try:
            likes = Like.objects.filter(user=request.user)
        except Like.DoesNotExist:
            likes = None
    else:
        likes = None
    if likes is not None:
        for post in posts:
            for like in likes:
                if like.post == post:
                    post.is_liked = True
                    break
                else:
                    post.is_liked = False
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{
        'posts':page_obj,

    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def new_post(request):
    if request.method == "POST":
        content = request.POST["new-post"]
        user = request.user

        post = Post(content=content, user=user)
        post.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))
    

    
def profile(request,user_id):
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    try:
        likes = Like.objects.filter(user=user)
    except Like.DoesNotExist:
        likes = None
    if likes is not None:
        for post in posts:
            for like in likes:
                if like.post == post:
                    post.is_liked = True
                    break
                else:
                    post.is_liked = False
    followed = False
    try:
        following = Following.objects.filter(user=user)
    except Following.DoesNotExist:
        following = None
    if following is not None:
        following = Following.objects.filter(user=user).all()
        following_number = len(following)
    else:
        following_number = 0
    try:
        follower = Follower.objects.filter(user=user)
    except Follower.DoesNotExist:
        follower = None
    if follower is not None:
        follower = Follower.objects.filter(user=user).all()
        follower_number = len(follower)
        for f in follower:
            if f.user == user:
                followed = True
                break
    else:
        follower_number = 0
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "requestUser": request.user,
        "profile_owner": user,
        "posts": page_obj,
        "following_number": following_number,
        "follower_number": follower_number,
        "followed": followed,
    })

def followUnfollow(request):
    if request.method == "POST":
        user = User.objects.get(id=request.POST["user_id"])
        owner = User.objects.get(id=request.POST["profile_owner_id"])
        try:
            following = Following.objects.filter(user=user).all()
        except Following.DoesNotExist:
            following = None
        
        if following is not None:
            following = Following.objects.filter(user=user).all()
            follow = True
            try:
                tmp = Follower.objects.get(user=owner, follower=user)
            except Follower.DoesNotExist:
                follow = False
            if follow:
                tmp = Follower.objects.get(user=owner, follower=user)
                tmp.delete()
                tmp2 = Following.objects.get(user=user, following=owner)
                tmp2.delete()
                return HttpResponseRedirect('/'+ str(owner.id))
            else:
                tmp = Follower(user=owner, follower=user)
                tmp.save()
                tmp2 = Following(user=user, following=owner)
                tmp2.save()
                return HttpResponseRedirect('/'+ str(owner.id))
        else:
            tmp = Follower(user=owner, follower=user)
            tmp.save()
            tmp2 = Following(user=user, following=owner)
            tmp2.save()
            return HttpResponseRedirect('/'+ str(owner.id))
        

def following_view(request):
    if request.user.is_authenticated:
        user = request.user
        posts = Post.objects.filter(user=user).order_by('-created_at')
        try:
            likes = Like.objects.filter(user=user)
        except Like.DoesNotExist:
            likes = None
        if likes is not None:
            for post in posts:
                for like in likes:
                    if like.post == post:
                        post.is_liked = True
                        break
                    else:
                        post.is_liked = False
        try:
            following = Following.objects.filter(user=user).all()
        except Following.DoesNotExist:
            following = None
            no_post = True
        if following is not None:
            posts = []
            for f in following:
                posts += Post.objects.filter(user=f.following).all()
            if posts == []:
                no_post = True
            else:
                no_post = False
                posts = sorted(posts, key=attrgetter('created_at'), reverse=True)
        else:
            no_post = True
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/following.html",
                      {"posts": page_obj, "no_post": no_post, "user": user})
    else:
        return render(request, "network/login.html", {
                "message": "Please login before go to 'Following' page."
            })
    

@login_required
@csrf_exempt
def editAndLike(request, post_id):
    if request.method == "PUT":
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)  
        if request.user == post.user:
            data = json.loads(request.body)
            if data.get("content") is not None:
                post.content = data["content"]
            if data.get("like") is not None:
                post.like += data["like"]
                user = post.user
                if data["like"] >0:
                    like = Like(post=post, user=user)
                    like.save()
                    return HttpResponse(status=200)
                else:
                    like = Like.objects.get(post=post, user=user)
                    like.delete()
                    return HttpResponse(status=200)
            post.save()
            return HttpResponse(status=200)
        else:
          return JsonResponse({"error": "Do not change other post."}, status=400)  
    else:
        return JsonResponse({"error": "POST request required."}, status=400)