import re

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.gis.geos import GEOSGeometry, Point
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .forms import PostForm
from .models import Post


class PostListView(ListView):
    queryset = Post.objects.all().select_related("author")

    def get_queryset(self):
        qs = super().get_queryset()

        center_xy = self.request.GET.get("center", "")
        if center_xy:
            try:
                # 위도: latitude, 경도: longitude
                latitude, longitude = re.findall(r"([\d]+\.?[\d]*)", center_xy)
                qs = qs.nearest(latitude, longitude, distance_meter=1000)
            except ValueError:
                pass

        return qs


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = "__all__"
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        y, x = 36.3679652, 127.388167  # 둔산대공원
        post.point = GEOSGeometry(f"POINT({x} {y})", srid=4326)
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    def test_func(self):
        post = self.get_object()
        return self.request.user.id == post.author
