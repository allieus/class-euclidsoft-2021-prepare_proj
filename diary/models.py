from django.conf import settings
from django.db import models
from django.contrib.gis.db.models import PointField


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    message = models.TextField()
    photo = models.ImageField(blank=True)
    point = PointField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
