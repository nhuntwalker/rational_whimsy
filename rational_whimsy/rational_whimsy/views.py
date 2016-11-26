"""View file for the home page."""
from django.shortcuts import render
from blog.models import Post


def home_view(request):
    """Simple view for the home page listing blog posts."""
    posts = Post.published.all()
    return render(request, "rational_whimsy/home.html", {"posts": posts})
