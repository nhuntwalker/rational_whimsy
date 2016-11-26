"""Views for the blog app."""
from django.shortcuts import render
from .models import Post


def list_posts(request):
    """Return a list of published blog posts."""
    posts = Post.published.all()
    return render(request, "blog/blog_list.html", {
        "posts": posts,
        "page": "blog"
    })


def post_detail(request, pk=None, slug=None):
    """Look at a single blog post in detail."""
    if slug:
        post = Post.published.get(slug=slug)
    elif pk:
        post = Post.published.get(pk=pk)
    else:
        return render(request, "notfound.html", {
            "page": "blog"
        })

    return render(request, "blog/blog_detail.html", {
        "page": "blog",
        "post": post
    })


def create_post(request):
    """Create a new blog post."""
    return render(request, "notfound.html", {
        "page": "blog"
    })


def edit_post(request, pk=None):
    """Edit an existing blog post."""
    return render(request, "notfound.html", {
        "page": "blog"
    })
