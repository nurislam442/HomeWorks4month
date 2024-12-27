from django.shortcuts import render, redirect
from django.http import HttpResponse
from posts.models import Post
from posts.forms import Post_Form, SearchForm, PostUpdateForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.
def hello_view(request):
    return HttpResponse("hello world")

def html_view(request):
    return render(request,"tea.html")

def main_view(request):
    return render(request, "main.html")

@login_required(login_url="login-view")
def list_view(request):
    if request.method == "GET":
        page = int(request.GET.get("page", 1))
        limit = 4
        search = request.GET.get("search")
        category = request.GET.get("category")
        ordering = request.GET.get("ordering")
        form = SearchForm(request.GET)
        posts = Post.objects.all()
        if search:
            posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))
        if category:
            posts = posts.filter(category_id=category)
        if ordering:
           max_pages = posts.order_by(ordering)
        max_pages = posts.count() / limit
        if round(max_pages) > max_pages:
            max_pages = round(max_pages) + 1
        else:
            max_pages = round(max_pages)
        start = (page - 1)*limit
        end = page * limit
        posts = posts[start:end]
        context = {"posts": posts, "form":form, "max_pages":range(1, max_pages + 1)}

        return render(request, "posts/post_list.html", context=context)

@login_required(login_url="login-view")
def detail_view(request, id):
    post = Post.objects.get(id=id)
    return render(request, "posts/post_detail.html", context={"post" : post})

@login_required(login_url="login-view")
def create_post(request):
    if request.method == "GET":
        form = Post_Form()
        return render(request, "posts/post_create.html", context={"form":form})
    if request.method == "POST":
        form = Post_Form(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "posts/post_create.html", context={"form":form})
        elif form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            rate = form.cleaned_data["rate"]
            image = form.cleaned_data["image"]
            post = Post.objects.create(title=title, content=content, rate=rate, image=image)
            return redirect("/posts/")
            
        # data = request.POST
        # image = request.FILES.get("image")
        # title = data.get("title")
        # content = data.get("content")
        # rate = data.get("rate")
@login_required(login_url="login-view")
def post_update(request, id):
    post = Post.objects.get(id=id, autor=request.user).first()
    if not post:
        return HttpResponse("you don't have permission to update this post or post does not exist")
    if request.method == "GET":
        form = PostUpdateForm(instance=post)
        return render(request, "posts/post_update.html", context = {"form":form})
    if request.method == "POST":
        form = PostUpdateForm(request.POST, request.FILES, instance=post)
        if not form.is_valid:
            return render(request, "posts/post_update.html", context = {"form":form})
        elif form.is_valid:
            form.save()
            return redirect(f"/post/{post.id}/")