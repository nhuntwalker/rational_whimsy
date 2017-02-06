from django.contrib import admin
from .models import Post
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    """Handle how the Post model appears in the admin."""

    fields = ("cover_img", "title", "slug", "published_date", "body", "status", "featured")
    list_display = ("title", "slug", "created", "published_date", "status")
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Post, PostAdmin)
