"""Views for the Profile app."""
from django.shortcuts import render
from my_profile.models import NMHWProfile
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

# Create your views here.


def profile_detail(request):
    """Show the detail for a single user profile."""
    profile = NMHWProfile.objects.get(user__username="nhuntwalker")
    return render(request, "my_profile/about.html", {"profile": profile})


class EditProfile(UpdateView):
    """Edit my profile."""

    model = NMHWProfile
    template_name = "my_profile/profile_edit_form.html"
    fields = ["photo", "linkedin", "github", "twitter",
              "facebook", "instagram", "description"]
    success_url = reverse_lazy("profile")
