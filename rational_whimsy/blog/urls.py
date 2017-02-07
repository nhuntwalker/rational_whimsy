"""URLs for the blog app."""

from django.conf.urls import url
from blog.views import (
    ListPosts,
    post_detail,
    CreatePost,
    EditPost,
    DeletePost
)

urlpatterns = [
    url(r'^$', ListPosts.as_view(), name="list_posts"),
    url(r'^new$', CreatePost.as_view(), name="create_posts"),
    url(
        r'^(?P<slug>[a-z0-9\-_]+)$',
        post_detail,
        name="post_detail_slug"
    ),
    url(r'^(?P<pk>[0-9]+)$', post_detail, name="post_detail_pk"),
    url(r'^(?P<pk>[0-9]+)/edit$', EditPost.as_view(), name="edit_post"),
    url(r'^(?P<pk>[0-9]+)/delete$', DeletePost.as_view(), name="delete_post")
]
