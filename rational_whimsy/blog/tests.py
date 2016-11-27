"""Tests of the blog app."""
from django.test import TestCase, Client
from django.utils.text import slugify
from .models import Post
import factory
import datetime

# Create your tests here.


class PostFactory(factory.Factory):
    """Generate new post objects."""

    class Meta:
        """Define the model to use as a base."""

        model = Post

    title = factory.Sequence(lambda x: "Post {} Foo".format(x))
    slug = factory.LazyAttribute(lambda x: slugify(x.title))
    body = factory.Sequence(
        lambda x: "This is the body for post number {}".format(x))
    created = datetime.datetime.now()
    modified = datetime.datetime.now()
    published_date = datetime.datetime.now()
    status = "published"


class BlogTestCase(TestCase):
    """Unit tests for the Post model."""

    def setUp(self):
        """Set up the test class."""
        self.new_posts = [PostFactory.create() for i in range(20)]

    def save_posts(self):
        """Save all the new posts created."""
        for post in self.new_posts:
            post.save()

    def test_str_is_title(self):
        """The string representation is the title of the post."""
        post = PostFactory.create()
        self.assertEqual(str(post), post.title)

    def test_posts_have_attrs(self):
        """Every post object should have the proper attributes."""
        post = PostFactory.create()
        all_attrs = ["title", "body", "created", "published_date",
                     "modified", "slug", "status", "featured"]
        for attr in all_attrs:
            self.assertTrue(hasattr(post, attr))

    def test_published_only_returns_published_posts(self):
        """The status of every post returned by Post.published is published."""
        for idx, item in enumerate(self.new_posts):
            if idx % 2:
                item.status = "draft"

            item.save()

        published = Post.published.all()
        self.assertEqual(len(published), 10)

    def test_published_returns_latest_first(self):
        """The first post returned by Post.published is latest."""
        self.save_posts()
        published = Post.published.all()
        self.assertEqual(self.new_posts[-1], published.first())

    def test_only_one_featured_post_at_a_time(self):
        """There may only be one featured post at a time."""
        self.save_posts()
        for idx, item in enumerate(self.new_posts):
            if idx % 2:
                item.featured = True
            item.save()

        featured = Post.objects.filter(featured=True).all()
        self.assertEqual(featured.count(), 1)


class BlogRoutesTestCase(TestCase):
    """Unit tests for the views in the Blog app."""

    def setUp(self):
        """Create new posts and set up a test client."""
        self.new_posts = [PostFactory.create() for i in range(20)]
        for post in self.new_posts:
            post.save()
        self.client = Client()

    def test_blog_list_returns_200(self):
        """Hitting the blog route returns a status 200."""
        response = self.client.get("/blog/")
        self.assertEqual(response.status_code, 200)

    def test_list_posts_gets_published_posts(self):
        """The posts in the context of the list view are all published."""
        # import pdb; pdb.set_trace()
        response = self.client.get("/blog/")
        self.assertEqual(len(self.new_posts),
                         response.context["posts"].count())

    def test_blog_roll_title_is_blog(self):
        """The title of the blog list should be blog."""
        response = self.client.get("/blog/")
        self.assertEqual(response.context["page"], "blog")

    def test_blog_roll_uses_right_template(self):
        """The blog roll should use the blog_list template."""
        response = self.client.get("/blog/")
        self.assertTemplateUsed(response, "layout.html")
        self.assertTemplateUsed(response, "blog/blog_list.html")

    def test_every_blog_detail_slug_returns_200(self):
        """Hitting the detail route for every post returns a status 200."""
        for post in self.new_posts:
            response = self.client.get("/blog/{}".format(post.slug))
            self.assertEqual(response.status_code, 200)

    def test_every_blog_detail_pk_returns_200(self):
        """Hitting the detail route for every post using the pk is 200."""
        for post in self.new_posts:
            response = self.client.get("/blog/{}".format(post.pk))
            self.assertEqual(response.status_code, 200)
