"""."""
from django.contrib import admin
from projects.models import (
    Project, Scripts, Data
)
# Register your models here.


def make_published(modeladmin, request, queryset):
    """Publish a set of projects."""
    queryset.update(status="published")


def make_private(modeladmin, request, queryset):
    """Change the status of a set of projects to private."""
    queryset.update(status="private")


make_published.short_description = "Mark selected stories as published."
make_private.short_description = "Mark selected stories as private."


class ProjectAdmin(admin.ModelAdmin):
    """Handle how the Project model appears in the admin."""

    fields = (
        "cover_img", "title", "slug",
        "published_date", "data_sets", "scripts", "body", "status",
        "featured", "tags"
    )
    list_display = ("title", "slug", "created", "published_date", "status")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["-published_date", "-created", "status"]
    actions = [make_published, make_private]


class AncillaryAdmin(admin.ModelAdmin):
    """Handle how the Scripts model appears in the admin."""

    list_display = ('name', 'upload_date')
    ordering = ["-upload_date"]

admin.site.register(Project, ProjectAdmin)
admin.site.register(Scripts, AncillaryAdmin)
admin.site.register(Data, AncillaryAdmin)
