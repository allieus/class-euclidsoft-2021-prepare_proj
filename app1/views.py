import pytz
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.cache import cache_page

from app1.models import Post


@cache_page(10)
def post_list(request: HttpRequest) -> HttpResponse:
    qs = Post.objects.all()
    current_time = timezone.now()\
        .replace(tzinfo=pytz.timezone("Asia/Seoul"))\
        .strftime("%Y-%m-%d %H:%M:%S")
    return render(request, "app1/post_list.html", {
        "post_list": qs,
        "current_time": current_time,
    })
