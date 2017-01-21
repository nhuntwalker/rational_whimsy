"""Views for the Profile app."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from my_profile.models import NMHWProfile
from my_profile.forms import EditProfileForm
# Create your views here.


def profile_detail(request):
    """Show the detail for a single user profile."""
    profile = NMHWProfile.objects.get(user__username="nhuntwalker")
    return render(request, "my_profile/about.html", {"profile": profile})


@login_required(login_url=reverse_lazy("login"))
def profile_edit(request):
    """Edit a single user profile."""
    profile = NMHWProfile.objects.get(user__username="nhuntwalker")
    form = EditProfileForm(instance=profile)
    if request.POST and request.method == "POST":
        new_form = EditProfileForm(request.POST, instance=profile)
        new_form.save()
        return redirect('profile')
    return render(request, "my_profile/profile_edit_form.html", {"form": form})
