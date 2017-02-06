"""Script for retrieving items from wordpress for input into Django."""
import django
from django.utils.text import slugify

import datetime
import os
import requests
import html

from blog.models import Post

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rational_whimsy.settings")
django.setup()


def make_new_post(the_dict):
    """Reduce the input dictionary to a selection of keys."""
    title = html.unescape(the_dict["title"]["rendered"])
    body = html.unescape(the_dict["content"]["rendered"])
    slug = slugify(title)
    fmt = "%Y-%m-%dT%H:%M:%S"
    date = datetime.datetime.strptime(the_dict["date"], fmt)
    new_post = Post(
        title=title,
        body=body,
        published_date=date,
        slug=slug
    )
    new_post.save()
    new_post.tags.add(*the_dict["tags"])
    new_post.save()


def run():
    """Run function for manage.py to see."""
    response = requests.get(
        "http://rationalwhimsy.com/wp-json/wp/v2/posts?per_page=100")
    posts = response.json()

    response = requests.get(
        "http://rationalwhimsy.com/wp-json/wp/v2/tags?per_page=100")
    tags = response.json()

    for post in posts:
        for idx, tag in enumerate(post["tags"]):
            find_tag = filter(lambda x: x["id"] == post["tags"][idx], tags)
            the_tag = list(find_tag)[0]["name"]
            post["tags"][idx] = the_tag
        make_new_post(post)
