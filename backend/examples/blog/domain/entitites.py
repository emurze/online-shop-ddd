from pydantic import Field

from auth.domain.value_objects import AccountId

from blog.domain.value_objects import AuthorId, PostId
from seedwork.domain.entities import AggregateRoot, LocalEntity
from seedwork.domain.value_objects import deferred, Deferred


class Author(LocalEntity):
    id: deferred[AuthorId] = Deferred
    account_id: AccountId


class Post(AggregateRoot):
    id: deferred[PostId] = Deferred
    author: Author
    title: str = Field(max_length=256)
    content: str = Field(max_length=256)
    draft: bool = False