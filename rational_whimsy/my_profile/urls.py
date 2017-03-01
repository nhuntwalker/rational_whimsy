"""URLs for the Profile app."""
from django.conf.urls import url
from my_profile.views import (
    profile_detail,
    profile_edit,
    get_github_events
)

urlpatterns = [
    url(r'^$', profile_detail, name="profile"),
    url(r'^edit$', profile_edit, name="profile_edit"),
    url(r'^get_github$', get_github_events, name="get_github")
]
