from django.db import models

# Create your models here.

PUBLICATION_STATUS = (
    ("published", "Published"),
    ("draft", "Draft")
)


class PostManager(models.Manager):
    """Retrieve all the published posts."""

    def get_queryset(self):
        """Alter the queryset returned."""
        return super(PostManager, self).get_queryset().filter(status="published")


class Post(models.Model):
    """The model for an individual blog post."""

    id = models.IntegerField(primary_key=True)
    title = models.CharField(name="title", max_length=255)
    body = models.TextField(name="body")
    created = models.DateTimeField(name="created", auto_now_add=True)
    published_date = models.DateTimeField(name="published_date")
    modified = models.DateTimeField(name="modified", auto_now=True)
    slug = models.SlugField(max_length=255, unique=True)

    status = models.CharField(
        name="status", choices=PUBLICATION_STATUS, default="draft", max_length=20)

    objects = models.Manager()
    published = PostManager()

    def __str__(self):
        return self.title