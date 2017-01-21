"""Tests for the Profile model and related views."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import get_user
from django.contrib.auth.models import User, AnonymousUser
from my_profile.models import NMHWProfile
import factory
from faker import Faker
from django.forms import ModelForm
from django.urls import reverse_lazy
from bs4 import BeautifulSoup
from django.contrib.sessions.middleware import SessionMiddleware


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
        self.user.set_password("potatoes")
        self.user.save()
        self.profile = self.user.profile
        self.client = Client()
        self.request = RequestFactory()
        self.get_req = RequestFactory().get("/foo_path")

    def add_session_middleware(self, request):
        """Need to add session middleware for authentication."""
        mdl = SessionMiddleware()
        mdl.process_request(request)
        request.session.save()
        request.user = self.user

    def test_profile_detail_view_has_details(self):
        """Information from the profile should be in the response."""
        from my_profile.views import profile_detail
        response = profile_detail(self.get_req)
        self.assertIn(self.profile.linkedin, str(response.content))
        self.assertIn(self.profile.twitter, str(response.content))
        self.assertIn(self.profile.github, str(response.content))
        self.assertIn(self.profile.instagram, str(response.content))

    def test_profile_detail_view_accesses_profile(self):
        """All of my profile's details should be in the view's context."""
        response = self.client.get(reverse_lazy("profile"))
        self.assertTrue(response.context["profile"] == self.profile)

    def test_profile_detail_view_accesses_correct_template(self):
        """The detail view should use the my_profile/about.html template."""
        response = self.client.get(reverse_lazy("profile"))
        self.assertTemplateUsed(response, "my_profile/about.html")

    def test_profile_login_route_get_shows_form(self):
        """A get request to the login route shows a login form."""
        response = self.client.get(reverse_lazy("login"))
        html = BeautifulSoup(response.content, "html5lib")
        self.assertTrue(html.find("form") is not None)

    def test_profile_login_route_has_proper_input_fields(self):
        """A get request shows all the proper fields, with required parts."""
        response = self.client.get(reverse_lazy("login"))
        html = BeautifulSoup(response.content, "html5lib")
        fields = ["username", "password"]
        for field in fields:
            self.assertTrue(html.find("input", {"name": field}) is not None)
        btn = html.find("input", {"name": "submit"})
        self.assertTrue(btn.attrs["value"] == "Log In")

    def test_profile_login_route_redirects(self):
        """When logging in with good credentials we redirect."""
        response = self.client.post(reverse_lazy("login"), {
            "username": self.user.username,
            "password": "potatoes"
        })
        self.assertTrue(response.status_code == 302)

    def test_profile_login_route_redirects_to_home(self):
        """When logging in with good credentials we reach home page."""
        response = self.client.post(reverse_lazy("login"), {
            "username": self.user.username,
            "password": "potatoes"
        })
        self.assertTrue(response.url == reverse_lazy("home_page"))

    def test_profile_login_route_logs_in_users(self):
        """A logged in user is authenticated."""
        self.client.post(reverse_lazy("login"), {
            "username": self.user.username,
            "password": "potatoes"
        })
        self.assertTrue(self.user.is_authenticated)

    def test_profile_edit_get_is_form(self):
        """A simple get request returns a form in HTML."""
        from my_profile.views import profile_edit
        self.get_req.user = self.user
        response = profile_edit(self.get_req)
        html = BeautifulSoup(response.content, "html5lib")
        self.assertTrue(len(html.find_all("form")) == 1)

    def test_profile_edit_form_has_fields(self):
        """A GET request returns all the form fields."""
        from my_profile.views import profile_edit
        self.get_req.user = self.user
        response = profile_edit(self.get_req)
        html = BeautifulSoup(response.content, "html5lib")
        desired_fields = ["linkedin", "github", "twitter",
                          "facebook", "instagram"]
        for field in desired_fields:
            self.assertTrue(html.find("input", {"name": field}) is not None)
        self.assertTrue(html.find("textarea",
                                  {"name": "description"}) is not None)
        self.assertTrue(html.find("select", {"name": "photo"}) is not None)

    def test_profile_edit_response_has_form_in_context(self):
        """A get request returns a form object in the context."""
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy("profile_edit"))
        self.assertIsInstance(response.context["form"], ModelForm)

    def test_profile_edit_form_with_post_redirects_on_success(self):
        """A post request redirects on success."""
        from my_profile.views import profile_edit
        post_req = self.request.post("/foo_path", {
            "photo": "",
            "linkedin": "",
            "github": "",
            "twitter": "",
            "facebook": "",
            "instagram": "",
            "description": "pancakes"
        })
        post_req.user = self.user
        response = profile_edit(post_req)
        self.assertTrue(response.status_code == 302)

    def test_profile_edit_route_with_post_redirects_to_profile(self):
        """A post request redirects to the profile page."""
        self.client.force_login(self.user)
        response = self.client.post(reverse_lazy("profile_edit"), {
            "photo": "",
            "linkedin": "",
            "github": "",
            "twitter": "",
            "facebook": "",
            "instagram": "",
            "description": "pancakes"
        }, follow=True)
        chain = response.redirect_chain
        self.assertTrue(chain[0][0] == reverse_lazy("profile"))

    def test_profile_edit_view_with_post_changes_model_attrs(self):
        """A post request to edit view changes the model attributes."""
        from my_profile.views import profile_edit
        post_req = self.request.post("/foo_path", {
            "photo": "",
            "linkedin": "",
            "github": "",
            "twitter": "",
            "facebook": "",
            "instagram": "",
            "description": "pancakes"
        })
        post_req.user = self.user
        profile_edit(post_req)
        profile = NMHWProfile.objects.get(user__username="nhuntwalker")
        self.assertTrue(profile.description == "pancakes")

    def test_profile_edit_route_with_post_changes_model_attrs(self):
        """A post request to the edit route changes the model attributes."""
        self.client.force_login(self.user)
        self.client.post(reverse_lazy("profile_edit"), {
            "photo": "",
            "linkedin": "",
            "github": "",
            "twitter": "",
            "facebook": "",
            "instagram": "",
            "description": "pancakes"
        })
        profile = NMHWProfile.objects.get(user__username="nhuntwalker")
        self.assertTrue(profile.description == "pancakes")

    def test_unauthenticated_user_profile_edit_route_redirects_login(self):
        """An unauthenticated user must be diverted from the edit route."""
        response = self.client.get(reverse_lazy("profile_edit"), follow=True)
        self.assertTrue(response.request["PATH_INFO"] == reverse_lazy("login"))

    def test_authorized_user_is_logged_out(self):
        """When a user is authenticated, logging them out logs them out."""
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy("logout"), follow=True)
        self.assertIsInstance(get_user(response.wsgi_request), AnonymousUser)
