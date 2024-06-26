import uuid
from dataclasses import field


def next_id() -> uuid.UUID:
    return uuid.uuid4()


def uuid_field(**kw):
    return field(default_factory=next_id, hash=True, **kw)
