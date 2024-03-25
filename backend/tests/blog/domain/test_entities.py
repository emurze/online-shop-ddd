import pytest

from blog.domain.entitites import Post
from seedwork.domain.pydantic_v1 import ValidationError


def test_validation() -> None:
    title = "lerka" * 100
    with pytest.raises(ValidationError):
        Post(title=title, content="content")
