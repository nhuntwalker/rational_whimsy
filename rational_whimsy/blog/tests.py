"""Tests of the blog app."""
from django.http.response import Http404
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse_lazy
from django.utils.text import slugify
from blog.models import Post
from django.contrib.auth.models import User
import factory
import datetime
from bs4 import BeautifulSoup
from faker import Faker

# Create your tests here.

fake = Faker()


class PostFactory(factory.Factory):
    """Generate new post objects."""

    class Meta:
        """Define the model to use as a base."""

        model = Post

    title = factory.Sequence(lambda x: "Post {} Foo".format(x))
    slug = factory.LazyAttribute(lambda x: slugify(x.title))
    body = factory.Sequence(
        lambda x: "This is the body for post number {}".format(x)
    )
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

    def test_saved_post_draft_gets_created_date(self):
        """."""
        post = Post(
            title="Test post",
            slug=slugify("test post"),
            body="Some body text for the sake of example.",
        )
        self.assertIsNone(post.created)
        post.save()
        self.assertIsInstance(post.created, datetime.datetime)

    def test_saved_post_published_gets_created_date(self):
        """."""
        post = Post(
            title="Test post",
            slug=slugify("test post"),
            body="Some body text for the sake of example.",
            status="Published"
        )
        self.assertIsNone(post.created)
        post.save()
        self.assertIsInstance(post.created, datetime.datetime)

    def test_published_only_returns_published_posts(self):
        """The status of every post returned by Post.published is published."""
        for idx, item in enumerate(self.new_posts):
            if idx % 2:
                item.status = "draft"

            item.save()

        published = Post.published.all()
        self.assertEqual(len(published), 10)

    def test_published_returns_latest_first(self):
        """The first post returned by Post.published is latest published."""
        self.save_posts()
        published = Post.published.all()
        sorted_posts = sorted(self.new_posts, key=lambda x: x.published_date)
        self.assertEqual(sorted_posts[0], published.first())

    def test_only_one_featured_post_at_a_time(self):
        """There may only be one featured post at a time."""
        self.save_posts()
        for idx, item in enumerate(self.new_posts):
            if idx % 2:
                item.featured = True
            item.save()

        featured = Post.objects.filter(featured=True).all()
        self.assertEqual(featured.count(), 1)


class BlogViewsUnitTests(TestCase):
    """Unit tests for the views in the Blog app."""

    def setUp(self):
        """Set up a test client."""
        self.client = Client()
        self.request_factory = RequestFactory()
        self.get_request = RequestFactory().get("/foo_path")
        user = User()
        user.username = "test_user"
        user.set_password("potatoes")
        self.user = user

    def add_posts(self):
        """Add some blog posts to the test DB."""
        new_posts = [PostFactory.create() for i in range(20)]
        for post in new_posts:
            post.save()
        self.new_posts = new_posts

    def add_mixed_posts(self):
        """Add some blog posts, some of which are drafts."""
        mixed_posts = [PostFactory.create() for i in range(6)]
        for idx, post in enumerate(mixed_posts):
            if (idx % 2):
                post.status = 'draft'
            post.save()
        self.mixed_posts = mixed_posts

    def test_list_posts_lists_the_posts(self):
        """The ListPosts view should actually include a list of blog posts."""
        from blog.views import ListPosts
        self.add_posts()
        request = self.request_factory.get("/fake-path")
        view = ListPosts.as_view(template_name="blog/blog_list.html")
        response = view(request)
        posts = response.context_data["object_list"]
        self.assertTrue(isinstance(posts[0], Post))

    def test_list_posts_has_blog_title(self):
        """The 'page' key in the response context is 'blog'."""
        from blog.views import ListPosts
        request = self.request_factory.get("/fake-path")
        view = ListPosts.as_view(template_name="blog/blog_list.html")
        response = view(request)
        self.assertTrue("page" in response.context_data)
        self.assertTrue(response.context_data["page"] == "blog")

    def test_list_posts_lists_only_published_posts(self):
        """The ListPosts view should include only published posts."""
        from blog.views import ListPosts
        self.add_mixed_posts()
        request = self.request_factory.get("/fake-path")
        view = ListPosts.as_view(template_name='blog/blog_list.html')
        response = view(request)
        posts = response.context_data["object_list"]
        self.assertTrue(len(posts) == Post.published.count())

    def test_post_detail_finds_primary_key(self):
        """The post_detail view should be able to take a primary key."""
        from blog.views import post_detail
        self.add_posts()
        request = self.request_factory.get("/fake-path")
        response = post_detail(request, pk=self.new_posts[0].id)
        this_post = Post.published.get(pk=self.new_posts[0].id)
        self.assertTrue(this_post.title in str(response.content))

    def test_post_detail_finds_slug(self):
        """You should be able to use a slug with the detail view."""
        from blog.views import post_detail
        self.add_posts()
        request = self.request_factory.get("/fake-path")
        response = post_detail(request, slug=self.new_posts[0].slug)
        self.assertTrue(response.status_code == 200)

    def test_edit_post_edits_existing_post(self):
        """The EditPost view should allow you to edit an existing post."""
        from blog.views import EditPost
        post = PostFactory.create()
        post.save()
        request = self.request_factory.post("/fake-path", {
            "title": "Edited This Post",
            "body": post.body,
            "status": post.status,
            "featured": post.featured
        })
        request.user = self.user
        view = EditPost.as_view(template_name="blog/blog_edit_form.html")
        view(request, pk=post.id)
        post = Post.published.first()
        self.assertTrue(post.title == "Edited This Post")

    def test_edit_post_bad_pk_is_404(self):
        """."""
        from blog.views import EditPost
        request = self.request_factory.post("/fake-path", {
            "title": "Edited This Post",
            "body": "flurb",
            "status": "draft",
            "featured": False
        })
        request.user = self.user
        view = EditPost.as_view(template_name="blog/blog_edit_form.html")
        with self.assertRaises(Http404):
            view(request, pk=2048)

    def test_delete_post_deletes_post(self):
        """The DeletePost view should delete the given post."""
        from blog.views import DeletePost
        post = PostFactory.create()
        post.save()
        request = self.request_factory.post("/fake-path")
        request.user = self.user
        view = DeletePost.as_view()
        view(request, pk=post.id)
        published = Post.published.all()
        self.assertTrue(len(published) == 0)

    def test_delete_post_bad_pk_is_404(self):
        """."""
        from blog.views import DeletePost
        request = self.request_factory.post("/fake-path")
        request.user = self.user
        view = DeletePost.as_view()
        with self.assertRaises(Http404):
            view(request, pk=2048)

    def test_create_post_creates_a_post(self):
        """The CreatePost view should create a new post."""
        from blog.views import CreatePost
        request = self.request_factory.post("/fake-path", {
            "title": "Test Create View",
            "body": "The body of a test post",
            "status": "published",
            "featured": False
        })
        request.user = self.user
        view = CreatePost.as_view(template_name="blog/blog_form.html")
        view(request)
        self.assertTrue(len(Post.published.all()) == 1)


class BlogRoutesTestCase(TestCase):
    """Unit tests for the routes in the Blog app."""

    def setUp(self):
        """Create new posts and set up a test client."""
        self.new_posts = [PostFactory.create() for i in range(20)]
        for post in self.new_posts:
            post.save()
        self.client = Client()
        user = User(username="test_user")
        user.set_password("potatoes")
        user.save()
        self.user = user

    def test_blog_list_returns_200(self):
        """Hitting the blog route returns a status 200."""
        response = self.client.get(reverse_lazy("list_posts"))
        self.assertEqual(response.status_code, 200)

    def test_list_posts_gets_published_posts(self):
        """The posts in the context of the list view are all published."""
        # import pdb; pdb.set_trace()
        response = self.client.get(reverse_lazy("list_posts"))
        self.assertTrue(response.context["object_list"].count() <= 5)

    def test_blog_roll_title_is_blog(self):
        """The title of the blog list should be blog."""
        response = self.client.get(reverse_lazy("list_posts"))
        self.assertEqual(response.context["page"], "blog")

    def test_blog_roll_uses_right_template(self):
        """The blog roll should use the blog_list template."""
        response = self.client.get(reverse_lazy("list_posts"))
        self.assertTemplateUsed(response, "layout.html")
        self.assertTemplateUsed(response, "blog/blog_list.html")

    def test_every_blog_detail_slug_returns_200(self):
        """Hitting the detail route for every post returns a status 200."""
        for post in self.new_posts:
            response = self.client.get(
                reverse_lazy(
                    "post_detail_slug",
                    kwargs={"slug": post.slug}
                )
            )
            self.assertEqual(response.status_code, 200)

    def test_blog_detail_bad_slug_returns_404(self):
        """."""
        response = self.client.get(
            reverse_lazy("post_detail_slug", kwargs={"slug": "foobar"})
        )
        self.assertEqual(response.status_code, 404)

    def test_every_blog_detail_pk_returns_200(self):
        """Hitting the detail route for every post using the pk is 200."""
        for post in self.new_posts:
            response = self.client.get(
                reverse_lazy(
                    "post_detail_pk",
                    kwargs={"pk": post.pk}
                )
            )
            self.assertEqual(response.status_code, 200)

    def test_blog_detail_bad_pk_returns_404(self):
        """."""
        response = self.client.get(
            reverse_lazy("post_detail_pk", kwargs={"pk": 1024})
        )
        self.assertEqual(response.status_code, 404)

    def test_create_route_has_form(self):
        """The create route has the appropriate form."""
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy("create_posts"))
        html = BeautifulSoup(response.content, "html5lib")
        self.assertTrue(html.find("form") is not None)

    def test_create_route_has_form_fields(self):
        """Create route has necessary fields for blog posts."""
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy("create_posts"))
        html = BeautifulSoup(response.content, "html5lib")
        self.assertTrue(html.find("input", {"name": "title"}) is not None)
        self.assertTrue(html.find("textarea", {"name": "body"}))

    def test_create_route_post_makes_new_post(self):
        """Create route makes a new post."""
        self.client.force_login(self.user)
        self.client.post(reverse_lazy("create_posts"), {
            "title": "Foo the Bar",
            "body": fake.paragraph(),
            "status": "draft"
        })
        self.assertTrue(Post.objects.count() == 21)

    def test_create_route_redirects_after_new_post(self):
        """Create route redirects after saving."""
        self.client.force_login(self.user)
        response = self.client.post(reverse_lazy("create_posts"), {
            "title": "Foo the Bar",
            "body": fake.paragraph(),
            "status": "draft"
        })
        self.assertTrue(response.status_code == 302)

    def test_edit_route_has_form(self):
        """."""
        self.client.force_login(self.user)
        this_post = self.new_posts[0]
        response = self.client.get(
            reverse_lazy("edit_post", kwargs={"pk": this_post.id})
        )
        html = BeautifulSoup(response.content, "html5lib")
        self.assertTrue(html.find("form") is not None)

    def test_edit_route_has_fields(self):
        """."""
        self.client.force_login(self.user)
        this_post = self.new_posts[0]
        response = self.client.get(
            reverse_lazy("edit_post", kwargs={"pk": this_post.id})
        )
        html = BeautifulSoup(response.content, "html5lib")
        self.assertTrue(html.find("input", {"name": "title"}) is not None)
        self.assertTrue(html.find("textarea", {"name": "body"}))

    def test_edit_route_post_redirects(self):
        """."""
        self.client.force_login(self.user)
        this_post = self.new_posts[0]
        response = self.client.post(
            reverse_lazy("edit_post", kwargs={"pk": this_post.id}),
            {
                "title": "Foo the Bar",
                "body": fake.paragraph(),
                "status": "draft"
            })
        self.assertTrue(response.status_code == 302)

    def test_edit_route_post_redirects_to_list_page(self):
        """."""
        self.client.force_login(self.user)
        this_post = self.new_posts[0]
        response = self.client.post(
            reverse_lazy("edit_post", kwargs={"pk": this_post.id}),
            {
                "title": "Foo the Bar",
                "body": fake.paragraph(),
                "status": "draft"
            }, follow=True)
        chain = response.redirect_chain
        self.assertTrue(reverse_lazy("list_posts") in chain[0])

    def test_delete_route_is_ok(self):
        """."""
        self.client.force_login(self.user)
        this_post = self.new_posts[0]
        response = self.client.get(
            reverse_lazy("delete_post", kwargs={"pk": this_post.id})
        )
        self.assertTrue(response.status_code == 200)

    def test_delete_route_confirms_delete(self):
        """."""
        self.client.force_login(self.user)
        this_post = self.new_posts[0]
        response = self.client.get(
            reverse_lazy("delete_post", kwargs={"pk": this_post.id})
        )
        check_str = "Are you sure you want to delete"
        self.assertTrue(check_str in str(response.content))

    def test_delete_route_post_removes_object(self):
        """."""
        self.client.force_login(self.user)
        this_post = self.new_posts[0]
        self.client.post(
            reverse_lazy("delete_post", kwargs={"pk": this_post.id})
        )
        self.assertTrue(Post.objects.count() == 19)

    def test_delete_route_post_redirects(self):
        """."""
        self.client.force_login(self.user)
        this_post = self.new_posts[0]
        response = self.client.post(
            reverse_lazy("delete_post", kwargs={"pk": this_post.id})
        )
        self.assertTrue(response.status_code == 302)

    def test_delete_route_post_redirects_to_post_list(self):
        """."""
        self.client.force_login(self.user)
        this_post = self.new_posts[0]
        response = self.client.post(
            reverse_lazy("delete_post",
                         kwargs={"pk": this_post.id}),
            follow=True
        )
        chain = response.redirect_chain
        self.assertTrue(reverse_lazy("list_posts") in chain[0])
