from django.conf import settings
from django.contrib.gis.db.models import Manager as GisManager
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db import models
from django.contrib.gis.db.models import PointField
from django.urls import reverse


# https://chang12.github.io/mysql-geospatial-index-1/
# https://chang12.github.io/mysql-geospatial-index-2/
class PostQuerySet(models.QuerySet):
    def nearest(
        self, latitude: float | str, longitude: float | str, distance_meter: int
    ):
        center = Point(float(latitude), float(longitude), srid=4326)
        qs = self.filter(point__distance_lte=(center, distance_meter))
        qs = qs.annotate(distance=Distance("point", center))
        qs = qs.order_by("distance")
        return qs


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+"
    )
    message = models.TextField()
    photo = models.ImageField(blank=True)
    point = PointField(db_index=True, srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GisManager.from_queryset(PostQuerySet)()

    def get_absolute_url(self):
        return reverse("diary:post_detail", args=[self.pk])
