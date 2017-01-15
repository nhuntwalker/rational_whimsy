"""View file for the home page."""
from django.shortcuts import render
from blog.models import Post


def home_view(request):
    """Simple view for the home page listing blog posts."""
    featured_post = Post.published.filter(featured=True).first()
    posts = Post.published.all().exclude(pk=featured_post.pk)[:5]
    return render(request, "rational_whimsy/home.html", {
        "posts": posts,
        "featured_post": featured_post
    })
