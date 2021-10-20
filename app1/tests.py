import pytest
from django.contrib.auth import get_user_model
from app1.models import Post


User = get_user_model()


@pytest.fixture
@pytest.mark.django_db
def general_user():
    return User.objects.create(username="user1")


@pytest.mark.django_db
def test_models(general_user):
    post = Post.objects.create(
        author=general_user,
        title="title",
        content="content",
    )
    assert post.pk == 1
