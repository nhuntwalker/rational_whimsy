"""Tests for the projects app."""
from django.test import TestCase

# Create your tests here.
import datetime
from django.utils.text import slugify
from projects.models import Project, Scripts, Data
import factory


class ProjectFactory(factory.Factory):
    """Generate new post objects."""

    class Meta:
        """Define the model to use as a base."""

        model = Project

    title = factory.Sequence(lambda x: "Project {} Foo".format(x))
    body = factory.Sequence(
        lambda x: "This is the body for project number {}".format(x)
    )
    created = datetime.datetime.now()
    modified = datetime.datetime.now()
    published_date = datetime.datetime.now()
    slug = factory.LazyAttribute(lambda x: slugify(x.title))
    status = "published"


class ProjectTestCase(TestCase):
    """Tests for the project model."""

    def test_projects_have_expected_fields(self):
        """The project model has all of the expected fields."""
        proj = ProjectFactory.create()
        all_attrs = [
            "title", "body", "created", "published_date",
            "modified", "slug", "status", "featured", "tags",
            "published"
        ]
        for attr in all_attrs:
            self.assertTrue(hasattr(proj, attr))
