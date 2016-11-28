"""URLs for the blog app."""

from django.conf.urls import url
from .views import list_posts, post_detail
# , create_post, edit_post

urlpatterns = [
    url(r'^$', list_posts, name="list"),
    # url(r'^new', create_post, name="create"),
    url(r'^(?P<slug>[a-z][a-z0-9\-_]+)', post_detail, name="detail_slug"),
    url(r'^(?P<pk>[0-9]+)', post_detail, name="detail_pk"),
    # url(r'^(?P<pk>[0-9]+)/edit', edit_post, name="edit")
]
