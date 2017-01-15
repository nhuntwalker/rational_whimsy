"""Views for the blog app."""
from django.shortcuts import render
from blog.models import Post
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class ListPosts(ListView):
    """List out all of the individual posts."""

    model = Post
    template_name = "blog/blog_list.html"

    def get_context_data(self, **kwargs):
        """Need to add a bit more context."""
        context = super(ListPosts, self).get_context_data(**kwargs)
        context["page"] = "blog"
        return context


def post_detail(request, pk=None, slug=None):
    """Look at a single blog post in detail."""
    if slug:
        post = Post.published.get(slug=slug)
    elif pk:
        post = Post.published.get(pk=pk)

    return render(request, "blog/blog_detail.html", {
        "page": "blog",
        "post": post
    })


class CreatePost(CreateView):
    """Create a new blog post."""

    model = Post
    fields = ["title", "body", "status", "featured"]
    template_name = "blog/blog_form.html"


class EditPost(UpdateView):
    """Edit an existing blog post."""

    model = Post
    template_name = "blog/blog_edit_form.html"
    fields = ["title", "body", "status", "featured"]


class DeletePost(DeleteView):
    """Delete an existing blog post."""

    model = Post
    success_url = reverse_lazy("home_page")
