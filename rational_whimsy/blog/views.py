"""Views for the blog app."""
from django.shortcuts import render


def list_posts(request):
    """Return a list of blog posts."""
    return render(request, "notfound.html", {})


def create_post(request):
    """Create a new blog post."""
    return render(request, "notfound.html", {})


def edit_post(request, id=None):
    """Edit an existing blog post."""
    return render(request, "notfound.html", {})


def post_detail(request, id=None, slug=None):
    """Look at a single blog post in detail."""
    return render(request, "notfound.html", {})
