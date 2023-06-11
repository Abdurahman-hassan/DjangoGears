from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from blog.models import Post


def index(request):
  # {{ post.published_at|date:"M, d Y" }}, {{ value|lower }}

    posts = Post.objects.filter(published_at__lte=timezone.now())
    return render(request, "blog/index.html", {"posts": posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post-detail.html", {"post": post})
