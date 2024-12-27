from django.shortcuts import render, redirect, HttpResponse
from user.forms import Registerform, LoginForm
from django.contrib.auth.models import User
from posts.models import Post
from user.models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def register_view(request):
    if request.method == "GET":
        form = Registerform
        return render(request, "user/register.html", context={"form":form})
    if request.method == "POST":
        form = Registerform(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "user/register.html", context={"form":form})
        elif form.is_valid():
            form.cleaned_data.__delitem__("password_confirm")
            image = form.cleaned_data.pop("image")
            age = form.cleaned_data.pop("age")
            # username = form.cleaned_data.get("username")
            # password = form.cleaned_data.get("password")
            user = User.objects.create_user(**form.cleaned_data)
                
            if user:
              Profile.objects.create(user=user, image=image, age=age)
            elif not user:
                form.add_error(None, "User wasn't created, something went wrong")
                return render(request, "user/register.html", context={"form":form}) 
            return redirect("main-page")
        
def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "user/login.html", context={"form":form})
    if request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, "user/login.html", context={"form":form})
        elif form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("/")
            if not user:
                form.add_error("username", "Invalid username or password")
                return render(request, "user/login.html", context={"form":form})
            
@login_required(login_url="login-view")
def logout_view(request):
    logout(request)
    return redirect("main-page")

@login_required(login_url="login-view")
def profile_view(request):
    user = request.user
    posts = Post.objects.filter(autor=user)
    return render(request, "user/profile.html", context={"user":user, "posts" : posts})
