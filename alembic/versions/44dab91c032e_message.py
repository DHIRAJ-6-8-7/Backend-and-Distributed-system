
"""Create initial tasks table."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "44dab91c032e"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the tasks table."""

    op.create_table(
        "tasks",
        sa.Column(
            "id",
            sa.Integer(),
            sa.Identity(always=False),
            primary_key=True,
            nullable=False,
        ),
        sa.Column("title", sa.String(100), nullable=False),
        sa.Column(
            "completed",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "age",
            sa.Integer(),
            server_default=sa.text("18"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Drop the tasks table."""

    op.drop_table("tasks")

