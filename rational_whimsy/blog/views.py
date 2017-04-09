"""Views for the blog app."""
from blog.models import Post

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class ListPosts(ListView):
    """List out all of the individual posts."""

    model = Post
    template_name = "blog/blog_list.html"
    queryset = Post.published.all()
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """Need to add a bit more context."""
        context = super(ListPosts, self).get_context_data(**kwargs)
        context["page"] = "blog"
        return context


def post_detail(request, pk=None, slug=None):
    """Look at a single blog post in detail."""
    if slug:
        post = get_object_or_404(Post, slug=slug)
    elif pk:
        post = get_object_or_404(Post, pk=pk)

    return render(request, "blog/blog_detail.html", {
        "page": "blog",
        "post": post
    })


class CreatePost(LoginRequiredMixin, CreateView):
    """Create a new blog post."""

    model = Post
    fields = ["title", "body", "status", "featured"]
    template_name = "blog/blog_form.html"
    success_url = reverse_lazy("list_posts")
    login_url = reverse_lazy("login")
    redirect_field_name = "redirect_to"


class EditPost(LoginRequiredMixin, UpdateView):
    """Edit an existing blog post."""

    model = Post
    template_name = "blog/blog_edit_form.html"
    fields = ["title", "body", "status", "featured"]
    success_url = reverse_lazy("list_posts")
    login_url = reverse_lazy("login")
    redirect_field_name = "redirect_to"


class DeletePost(LoginRequiredMixin, DeleteView):
    """Delete an existing blog post."""

    model = Post
    success_url = reverse_lazy("list_posts")
    login_url = reverse_lazy("login")
    redirect_field_name = "redirect_to"
