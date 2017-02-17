from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    """Task Datamodel"""
    user = models.ForeignKey(User, related_name="creator")
    title = models.CharField(max_length=128)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True)
    is_done = models.BooleanField(default=False)
    status_changed_by = models.ForeignKey(User, default=None, null=True,
                                          blank=True,
                                          related_name="changed_by")

    def __unicode__(self):
        return self.title
