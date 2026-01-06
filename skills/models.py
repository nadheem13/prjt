from django.db import models
from django.conf import settings

class Skill(models.Model):
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='skills')
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    availability = models.CharField(max_length=255, help_text="e.g., Weekends, Mon-Fri evenings")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
