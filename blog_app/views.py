from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView
from markdown import markdown
from .models import Post, Tag
from .forms import PostForm, UserRegisterForm


"""
TODO
No register avaible
hacker theme
"""


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class LoginView(auth_views.LoginView):
    template_name = "registration/login.html"


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("login")


def post_list(request):
    # posts = Post.objects.filter(published_date__isnull=False).order_by("published_date")
    posts = Post.objects.order_by("published_date")
    tags = Tag.objects.all()
    return render(request, "blog_app/post_list.html", {"posts": posts, "tags": tags})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # post.content = markdown(post.content, extensions=["fenced_code"])
    return render(request, "blog_app/post_detail.html", {"post": post})


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
    return render(request, "blog_app/post_form.html", {"form": form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                form.save_m2m()
                return redirect("post_detail", pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, "blog_app/post_form.html", {"form": form})
    else:
        return redirect("post_list")


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
        return redirect("post_list")
    else:
        return redirect("post_list")


def tag_posts(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    posts = Post.objects.filter(tags=tag)
    return render(
        request, "blog_app/post_list.html", {"posts": posts, "tags": Tag.objects.all()}
    )
