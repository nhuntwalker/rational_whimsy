"""URLs for the projects app."""

from django.conf.urls import url
from projects.views import (
    ListProjects,
    ListTaggedProjects,
    ProjectDetail,
)

urlpatterns = [
    url(r'^$', ListProjects.as_view(), name="list_posts"),
    url(
        r'^(?P<pk>[0-9]+)$',
        ProjectDetail.as_view(),
        name="post_detail_pk"
    ),
    url(
        r'^(?P<slug>[a-z0-9\-_]+)$',
        ProjectDetail.as_view(),
        name="post_detail_slug"
    ),
    url(
        r'^tagged/(?P<tag>[a-z0-9\-_(\%20)\s]+)',
        ListTaggedProjects.as_view(),
        name="projects_tagged_as"
    )
]
