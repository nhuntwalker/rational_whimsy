from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from blog_images.models import Image
# Create your models here.


class NMHWProfile(models.Model):
    """The layout for my profile model."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="profile"
    )
    photo = models.ForeignKey(
        Image,
        related_name="+",
        null=True,
        blank=True
    )
    linkedin = models.CharField(max_length=42, blank=True, default="")
    github = models.CharField(max_length=42, blank=True, default="")
    twitter = models.CharField(max_length=42, blank=True, default="")
    facebook = models.CharField(max_length=42, blank=True, default="")
    instagram = models.CharField(max_length=42, blank=True, default="")
    description = models.TextField(max_length=42, blank=True, default="")


@receiver(post_save, sender=User)
def auto_create_profile(sender, **kwargs):
    """Automatically create a profile when a user is created."""
    if kwargs["instance"] and not hasattr(kwargs["instance"], "profile"):
        new_user = kwargs["instance"]
        new_profile = NMHWProfile(user=new_user)
        new_profile.save()
