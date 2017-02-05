"""Site administration for the profile model."""
from django.contrib import admin
from my_profile.models import NMHWProfile

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    """Administrator for my Profile."""

    class Meta:
        """Meta for model."""

        model = NMHWProfile

admin.site.register(NMHWProfile, ProfileAdmin)
