"""Views for the Profile app."""
from django.shortcuts import render, redirect

from my_profile.models import NMHWProfile
from my_profile.forms import EditProfileForm
# Create your views here.


def profile_detail(request):
    """Show the detail for a single user profile."""
    profile = NMHWProfile.objects.get(user__username="nhuntwalker")
    return render(request, "my_profile/about.html", {"profile": profile})


def profile_edit(request):
    """Edit a single user profile."""
    profile = NMHWProfile.objects.get(user__username="nhuntwalker")
    form = EditProfileForm(instance=profile)
    if request.POST and request.method == "POST":
        new_form = EditProfileForm(request.POST, instance=profile)
        new_form.save()
        return redirect('profile')
    return render(request, "my_profile/profile_edit_form.html", {"form": form})
