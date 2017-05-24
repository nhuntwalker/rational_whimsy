"""."""
from django.contrib import admin
from .models import Post
# Register your models here.


def make_published(modeladmin, request, queryset):
    """Publish a set of posts."""
    queryset.update(status="published")


def make_private(modeladmin, request, queryset):
    """Change the status of a set of posts to private."""
    queryset.update(status="private")


make_published.short_description = "Mark selected stories as published."
make_private.short_description = "Mark selected stories as private."


class PostAdmin(admin.ModelAdmin):
    """Handle how the Post model appears in the admin."""

    fields = ("cover_img", "title", "slug", "published_date", "body", "status", "featured", "tags")
    list_display = ("title", "slug", "created", "published_date", "status")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["-published_date", "-created", "status"]
    actions = [make_published, make_private]

admin.site.register(Post, PostAdmin)
