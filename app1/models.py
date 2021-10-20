from django.conf import settings
from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(TimestampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    photo = models.ImageField(blank=True)
    tags = models.ManyToManyField("Tag", blank=True)

    def __str__(self):
        return self.title


class Comment(TimestampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()


class Tag(TimestampedModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
