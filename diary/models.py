import os
from typing import Type
from uuid import uuid4

from django.conf import settings
from django.contrib.gis.db.models import Manager as GisManager
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db import models
from django.contrib.gis.db.models import PointField
from django.urls import reverse
from django.utils import timezone


def uuid_name_upload_to(instance: Type[models.Model], filename):
    app_label = instance.__class__._meta.app_label  # 앱 이름을 디렉토리 경로명으로 사용
    cls_name = instance.__class__.__name__.lower()  # 모델 이름을 디렉토리 경로명으로 사용
    ymd_path = timezone.now().strftime("%Y/%m/%d")  # 업로드하는 년/월/일을 디렉토리 경로명으로 사용
    uuid_name = uuid4().hex  # 16진수 포맷의 랜덤한 32글자 문자열
    extension = os.path.splitext(filename)[-1].lower()  # 확장자 추출하고, 소문자로 변환. ex) ".jpg"
    return "/".join(
        [
            app_label,
            cls_name,
            ymd_path,
            uuid_name[:2],  # uuid의 처음 2문자를 별도 디렉토리 명으로 사용
            uuid_name + extension,
        ]
    )


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
    photo = models.ImageField(blank=True, upload_to=uuid_name_upload_to)
    point = PointField(db_index=True, srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GisManager.from_queryset(PostQuerySet)()

    def get_absolute_url(self):
        return reverse("diary:post_detail", args=[self.pk])
