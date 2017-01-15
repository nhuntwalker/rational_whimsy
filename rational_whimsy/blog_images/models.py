from django.db import models

# Create your models here.


class Image(models.Model):
    """The Image Model Object."""

    file = models.ImageField(
        upload_to="image_%m_%d_%Y_%H%M%S",
        null=True,
        blank=True
    )
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=2048)
    date_uploaded = models.DateTimeField(auto_now_add=True)
