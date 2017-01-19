"""URLs for the Profile app."""
from django.conf.urls import url
from my_profile.views import (
    profile_detail,
    EditProfile
)

urlpatterns = [
    url(r'^$', profile_detail, name="profile"),
]
