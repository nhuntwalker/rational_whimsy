"""Tests for the Profile model and related views."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from my_profile.models import NMHWProfile
import factory
from faker import Faker

fake = Faker()

# Create your tests here.


class UserFactory(factory.Factory):
    """Generate new User objects."""

    class Meta:
        """Define the model to base the factory on."""

        model = User

    username = fake.color_name()
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()


class ProfileModelTests(TestCase):
    """Tests of the profile model object."""

    def setUp(self):
        """Initial Setup."""
        pass

    def test_profile_is_made_when_user_is_saved(self):
        """When a user object is saved, a new profile is made."""
        new_user = UserFactory.create()
        new_user.save()
        self.assertTrue(NMHWProfile.objects.count() == 1)

    def test_only_one_profile_created_per_user(self):
        """The receiver dictates that on any save a profile is created.

        Make sure that only one profile gets created.
        """
        new_user = UserFactory.create()
        new_user.save()
        profile = NMHWProfile.objects.first()
        new_user.set_password("flibbertygibbet")
        new_user.save()
        self.assertTrue(new_user.profile == profile)


class ProfileViewTests(TestCase):
    """Tests for views associated with the profile model."""

    def setUp(self):
        """Set up a test user, profile, client, and requests."""
        self.user = UserFactory.create()
        self.user.username = "nhuntwalker"
        self.user.save()
        self.profile = self.user.profile
        self.client = Client()
        self.request = RequestFactory()

    def test_profile_detail_view_has_details(self):
        """Information from the profile should be in the response."""
        from my_profile.views import profile_detail
        request = self.request.get("/foo_path")
        response = profile_detail(request)
        self.assertIn(self.profile.linkedin, str(response.content))
        self.assertIn(self.profile.twitter, str(response.content))
        self.assertIn(self.profile.github, str(response.content))
        self.assertIn(self.profile.instagram, str(response.content))

    def test_profile_detail_view_accesses_profile(self):
        """All of my profile's details should be in the view's context."""
        response = self.client.get("/about_me")
        self.assertTrue(response.context["profile"] == self.profile)
