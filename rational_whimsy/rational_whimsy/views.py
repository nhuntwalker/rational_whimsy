"""View file for the home page."""
from django.shortcuts import render
from blog.models import Post


def home_view(request):
    """Simple view for the home page listing blog posts."""
    featured_post = Post.published.filter(featured=True).first()
    posts = Post.published.all().exclude(pk=featured_post.pk)[:3]
    return render(request, "rational_whimsy/home.html", {
        "posts": posts,
        "featured_post": featured_post
    })


def not_found(request):
    """Handler for a custom 404 page."""
    featured_post = Post.published.filter(featured=True).first()
    return render(request, "rational_whimsy/404.html", {
        "featured_post": featured_post
    })
