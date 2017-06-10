"""Tests for the projects app."""
from django.test import TestCase

# Create your tests here.
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.text import slugify
import os
from projects.models import Project, Scripts, Data
import factory

HERE = os.path.dirname(__file__)


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

    def test_str_is_title(self):
        """The string representation is the title of the project."""
        proj = ProjectFactory.create()
        self.assertEqual(str(proj), proj.title)

    def test_projects_have_expected_fields(self):
        """The project model has all of the expected fields."""
        proj = ProjectFactory.create()
        all_attrs = [
            "title", "body", "created", "published_date",
            "modified", "slug", "status", "featured",
        ]
        for attr in all_attrs:
            self.assertTrue(hasattr(proj, attr))

    def test_project_can_be_featured(self):
        """A project instance can be a featured project."""
        proj = ProjectFactory.create()
        proj.featured = True
        proj.save()
        self.assertTrue(proj.featured)

    def test_only_one_project_can_be_featured(self):
        """Only one project can be featured at a time."""
        proj1 = ProjectFactory.create()
        proj2 = ProjectFactory.create()
        proj1.featured = True
        proj1.save()
        proj2.featured = True
        proj2.save()
        f_count = Project.objects.filter(featured=True).count()
        self.assertEquals(f_count, 1)


class ScriptsTestCase(TestCase):
    """Tests for the scripts model."""

    def setUp(self):
        """Set up for the following tests."""
        with open(os.path.join(HERE, 'sample.js'), 'rb') as infile:
            self.data_file = SimpleUploadedFile('sample.js', infile.read())
            self.project = ProjectFactory.create()
            self.project.save()

    def tearDown(self):
        """Cleaning after all tests have finished running."""
        proj_root = os.path.dirname(HERE)
        scripts_dir = os.path.join(
            proj_root, 'MEDIA_ASSETS', 'project_scripts'
        )
        os.system('rm -rf {}'.format(scripts_dir))

    def test_scripts_have_expected_fields(self):
        """The script model has all of the expected fields."""
        script = Scripts(
            name='example_script',
            file=self.data_file,
            project=self.project
        )
        script.save()
        all_attrs = [
            "name", "upload_date", "file", "project"
        ]
        for attr in all_attrs:
            self.assertTrue(hasattr(script, attr))

    def test_projects_can_access_scripts(self):
        """The project a script is attached to can see its scripts."""
        script = Scripts(
            name='example_script',
            file=self.data_file,
            project=self.project
        )
        script.save()
        self.assertEquals(self.project.scripts.first(), script)


class DataTestCase(TestCase):
    """Tests for the data model."""

    def setUp(self):
        """Set up for the following tests."""
        with open(os.path.join(HERE, 'sample.csv'), 'rb') as infile:
            self.data_file = SimpleUploadedFile('sample.csv', infile.read())
            self.project = ProjectFactory.create()
            self.project.save()

    def tearDown(self):
        """Cleaning after all tests have finished running."""
        proj_root = os.path.dirname(HERE)
        data_dir = os.path.join(
            proj_root, 'MEDIA_ASSETS', 'project_data'
        )
        os.system('rm -rf {}'.format(data_dir))

    def test_data_has_expected_fields(self):
        """The data model has all of the expected fields."""
        data = Data(
            name='example_data',
            file=self.data_file,
            project=self.project
        )
        data.save()
        all_attrs = [
            "name", "upload_date", "file", "project"
        ]
        for attr in all_attrs:
            self.assertTrue(hasattr(data, attr))

    def test_projects_can_access_data(self):
        """The project a data file is attached to can see its data."""
        data = Data(
            name='example_data',
            file=self.data_file,
            project=self.project
        )
        data.save()
        self.assertEquals(self.project.data_sets.first(), data)
