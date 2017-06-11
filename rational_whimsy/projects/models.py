"""The Coding Project model."""
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from redactor.fields import RedactorField
from taggit.managers import TaggableManager

# Create your models here.


class Scripts(models.Model):
    """Model for individual javascript files."""

    name = models.CharField(name="name", max_length=255)
    upload_date = models.DateTimeField(name="upload_date", auto_now_add=True)
    file = models.FileField(
        upload_to="project_scripts",
    )

    class Meta:

        verbose_name_plural = 'scripts'


class Data(models.Model):
    """Model for individual data files."""

    name = models.CharField(name="name", max_length=255)
    upload_date = models.DateTimeField(name="upload_date", auto_now_add=True)
    file = models.FileField(
        upload_to="project_data"
    )

    class Meta:

        verbose_name_plural = 'data'


PUBLICATION_STATUS = (
    ("published", "Published"),
    ("draft", "Draft"),
    ("private", "Private")
)


class ProjectManager(models.Manager):
    """Retrieve all the published posts in reverse date order."""

    def get_queryset(self):
        """Alter the queryset returned."""
        return super(
            ProjectManager,
            self
        ).get_queryset().filter(status="published").order_by("-created")


class Project(models.Model):
    """The model for an individual project."""

    title = models.CharField(name="title", max_length=255)
    cover_img = models.ImageField(
        upload_to="project_covers",
        default="post_covers/stock-cover.jpg"
    )
    body = RedactorField(verbose_name="body")
    created = models.DateTimeField(name="created", auto_now_add=True)
    published_date = models.DateTimeField(
        name="published_date",
        blank=True,
        null=True
    )
    modified = models.DateTimeField(name="modified", auto_now=True)
    slug = models.SlugField(max_length=255, unique=True)

    status = models.CharField(
        name="status", choices=PUBLICATION_STATUS,
        default="draft", max_length=20)

    featured = models.BooleanField(default=False)
    objects = models.Manager()
    published = ProjectManager()
    tags = TaggableManager()
    scripts = models.ForeignKey(
        Scripts, on_delete=models.CASCADE, related_name="project",
        blank=True, null=True
    )
    data_sets = models.ForeignKey(
        Data, on_delete=models.CASCADE, related_name="project",
        blank=True, null=True
    )

    def __str__(self):
        """The string representation of the object."""
        return self.title


@receiver(post_save, sender=Project)
def unfeature_project(sender, **kwargs):
    """Reset feature status when saved project is featured.

    When a project is saved (either added or edited), if it's checked as being
    featured then make every/any other featured project unfeatured.
    """
    if kwargs["instance"].featured:
        other_projects = Project.objects.exclude(pk=kwargs["instance"].pk)
        for project in other_projects:
            project.featured = False
            project.save()
