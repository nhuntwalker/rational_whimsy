from django.contrib import admin
from .models import Post
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    """Handle how the Post model appears in the admin."""
    list_display = ("title", "slug", "created", "status")
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Post, PostAdmin)
