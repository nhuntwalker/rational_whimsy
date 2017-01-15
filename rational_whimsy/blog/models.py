from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

PUBLICATION_STATUS = (
    ("published", "Published"),
    ("draft", "Draft"),
    ("private", "Private")
)


class PostManager(models.Manager):
    """Retrieve all the published posts."""

    def get_queryset(self):
        """Alter the queryset returned."""
        return super(PostManager,
                     self).get_queryset().filter(status="published").order_by("-created")


class Post(models.Model):
    """The model for an individual blog post."""

    title = models.CharField(name="title", max_length=255)
    body = models.TextField(name="body")
    created = models.DateTimeField(name="created", auto_now_add=True)
    published_date = models.DateTimeField(name="published_date", blank=True, null=True)
    modified = models.DateTimeField(name="modified", auto_now=True)
    slug = models.SlugField(max_length=255, unique=True)

    status = models.CharField(
        name="status", choices=PUBLICATION_STATUS,
        default="draft", max_length=20)

    featured = models.BooleanField(default=False)
    objects = models.Manager()
    published = PostManager()

    def __str__(self):
        """The string representation of the object."""
        return self.title


@receiver(post_save, sender=Post)
def unfeature_posts(sender, **kwargs):
    """When a post is saved or edited and it's a featured post make all others no longer featured."""
    if kwargs["instance"].featured:
        other_posts = Post.objects.exclude(pk=kwargs["instance"].pk)
        for post in other_posts:
            post.featured = False
            post.save()
