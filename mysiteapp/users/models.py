from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # One-to-one relationship with User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Extra fields
    profile_image = models.ImageField(
        upload_to='profile_images/',
        default='profile_images/default_profile_pic.png',   # <-- default image inside media/profile_images/
        blank=True,
        null=True
    )

    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username