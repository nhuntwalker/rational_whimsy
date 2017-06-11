"""Tests for the projects app."""
from django.test import TestCase, Client, RequestFactory

# Create your tests here.
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.text import slugify
import factory
import os
from projects.models import (
    Project, Scripts, Data
)

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


class ProjectViewsUnitTests(TestCase):
    """Unit tests for the views of the projects app."""

    def setUp(self):
        """Set up a test client."""
        self.client = Client()
        self.request_factory = RequestFactory()
        self.get_req = RequestFactory().get('/foo')

    def add_projects(self):
        """Add some projects to be used for testing views."""
        [ProjectFactory.create().save() for i in range(20)]

    def add_mixed_projects(self):
        """Add some projects, some of which are drafts."""
        mixed_projs = [ProjectFactory.create() for i in range(6)]
        for idx, proj in enumerate(mixed_projs):
            if (idx % 2):
                proj.status = 'draft'
            proj.save()

    def test_list_projects_lists_project_objects(self):
        """The ListProjects view should include a list of project objects."""
        from projects.views import ListProjects
        self.add_projects()
        view = ListProjects.as_view()
        response = view(self.get_req)
        projects = response.context_data["object_list"]
        self.assertTrue(isinstance(projects[0], Project))

    def test_list_projects_page_name_is_projects(self):
        """The type of page we're looking at should be a project page."""
        from projects.views import ListProjects
        view = ListProjects.as_view()
        response = view(self.get_req)
        self.assertTrue(response.context_data['page'] == 'projects')

    def test_list_projects_page_only_shows_five(self):
        """The ListProjects view only shows five projects at a time."""
        from projects.views import ListProjects
        self.add_projects()
        view = ListProjects.as_view()
        response = view(self.get_req)
        projects = response.context_data["object_list"]
        self.assertTrue(len(projects) == 5)

    def test_list_projects_page_only_shows_published(self):
        """The ListProjects view only shows published projects."""
        from projects.views import ListProjects
        self.add_mixed_projects()
        view = ListProjects.as_view()
        response = view(self.get_req)
        projects = response.context_data['object_list']
        self.assertTrue(len(projects) == 3)

    def test_list_tagged_projects_only_shows_projects_with_tag(self):
        """The ListTaggedProjects view shows projects matching a tag."""
        from projects.views import ListTaggedProjects
        self.add_projects()
        projs = Project.published.all()
        for proj in projs[:3]:
            proj.tags.add('data')
            proj.save()
        view = ListTaggedProjects.as_view()
        response = view(self.get_req, **{'tag': 'data'})
        short_projects = response.context_data['object_list']
        self.assertTrue(len(short_projects) == 3)

    def test_project_detail_contains_project_info(self):
        """The ProjectDetail view just accesses and shows one project."""
        from projects.views import ProjectDetail
        self.add_projects()
        proj = Project.published.order_by('?').first()
        view = ProjectDetail.as_view()
        response = view(self.get_req, **{'pk': proj.pk})
        self.assertTrue(response.context_data['project'] == proj)

    def test_project_detail_can_use_slug(self):
        """The ProjectDetail view just accesses and shows one project."""
        from projects.views import ProjectDetail
        self.add_projects()
        proj = Project.published.order_by('?').first()
        view = ProjectDetail.as_view()
        response = view(self.get_req, **{'slug': proj.slug})
        self.assertTrue(response.context_data['project'] == proj)
