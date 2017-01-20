"""Forms for the my_profile app."""
from django.forms import ModelForm
from my_profile.models import NMHWProfile


class EditProfileForm(ModelForm):
    """Form for editing an indiviudal profile."""

    class Meta:
        """Declare the model to base this form on."""

        model = NMHWProfile
        fields = ["photo", "linkedin", "github", "twitter",
                  "facebook", "instagram", "description"]
