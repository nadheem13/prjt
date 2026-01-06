from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_provider = models.BooleanField(default=False, help_text="Designates whether this user can provide skills.")
    is_learner = models.BooleanField(default=False, help_text="Designates whether this user wants to learn skills.")
    bio = models.TextField(blank=True, help_text="Short bio about the user.")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username
