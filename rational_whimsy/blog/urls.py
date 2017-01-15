"""URLs for the blog app."""

from django.conf.urls import url
from blog.views import ListPosts, post_detail, CreatePost
# , create_post, edit_post

urlpatterns = [
    url(r'^$', ListPosts.as_view(), name="list"),
    url(r'^new', CreatePost.as_view(), name="create"),
    url(r'^(?P<slug>[a-z][a-z0-9\-_]+)', post_detail, name="detail_slug"),
    url(r'^(?P<pk>[0-9]+)', post_detail, name="detail_pk"),
    # url(r'^(?P<pk>[0-9]+)/edit', edit_post, name="edit")
]
