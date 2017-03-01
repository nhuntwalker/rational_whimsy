"""Views for the Profile app."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from my_profile.models import NMHWProfile
from my_profile.forms import EditProfileForm
from my_profile.serializers import EventSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response

from datetime import datetime
import os
import requests

# Create your views here.

API_KEY = os.environ.get('GITHUB_API_TOKEN', '')
FMT = '%Y-%m-%dT%H:%M:%SZ'
HEADERS = {'Authorization': 'token {}'.format(API_KEY)}


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


@api_view(['GET'])
def get_github_events(request):
    """Retrieve repositories from Github and return JSON."""
    api_url = 'https://api.github.com/users/nhuntwalker/events'
    api_url += '?q=""&per_page=100'
    resp = requests.get(api_url, headers=HEADERS)
    events = resp.json()
    repo_names = []
    repo_list = []
    idx = 0
    while len(repo_names) < 5 and idx < len(events):
        event = events[idx]
        if event["repo"]["name"] not in repo_names and event['public']:
            new_data = {}
            name = event["repo"]["name"]
            url = event["repo"]["url"]
            repo_names.append(name)
            info = get_repo_info(url)
            event_date = event["created_at"]
            creation_date = info["created_at"]

            new_data["name"] = name
            new_data["description"] = info["description"]
            new_data["repo_url"] = info["html_url"]
            new_data["updated_at"] = datetime.strptime(event_date, FMT)
            new_data["created_at"] = datetime.strptime(creation_date, FMT)
            new_data["stargazers_count"] = info["stargazers_count"]
            new_data["watchers_count"] = info["watchers_count"]
            new_data["forks"] = info["forks"]
            new_data["open_issues"] = info["open_issues"]
            repo_list.append(new_data)
        idx += 1

    serializer = EventSerializer(repo_list, many=True)
    return Response(serializer.data)


def get_repo_info(url):
    """Given a repo URL, get that repository's info."""
    resp = requests.get(url, headers=HEADERS)
    return resp.json()
