"""empty message

Revision ID: 48dc643174e7
Revises: e652f02b3ae2
Create Date: 2024-03-02 12:18:21.941910

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "48dc643174e7"
down_revision: Union[str, None] = "e652f02b3ae2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "client", "username", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "client",
        "date_joined",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
        existing_server_default=sa.text("timezone('utc'::text, now())"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "client",
        "date_joined",
        existing_type=postgresql.TIMESTAMP(),
        nullable=True,
        existing_server_default=sa.text("timezone('utc'::text, now())"),
    )
    op.alter_column(
        "client", "username", existing_type=sa.VARCHAR(), nullable=True
    )
    # ### end Alembic commands ###
