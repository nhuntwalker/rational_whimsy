"""URLs for the blog app."""

from django.conf.urls import url
from .views import list_posts, create_post, edit_post, post_detail

urlpatterns = [
    url(r'^$', list_posts, name="list"),
    url(r'^new', create_post, name="create"),
    url(r'^(?P<slug>[a-z\-_]+)', post_detail, name="detail_slug"),
    url(r'^(?P<id>[0-9]+)', post_detail, name="detail_id"),
    url(r'^(?P<id>[0-9]+)/edit', edit_post, name="edit")
]
