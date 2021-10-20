from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .forms import PostForm
from .models import Post


class PostListView(ListView):
    queryset = Post.objects.all().select_related("author")


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = "__all__"
    form_class = PostForm


class PostDetailView(DetailView):
    model = Post


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    def test_func(self):
        post = self.get_object()
        return self.request.user.id == post.author
