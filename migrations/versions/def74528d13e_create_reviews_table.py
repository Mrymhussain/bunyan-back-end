"""Create reviews table

Revision ID: def74528d13e
Revises: cf44539cf306
Create Date: 2026-10-05 11:09:45.259053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "def74528d13e"
down_revision: Union[str, Sequence[str], None] = "cf44539cf306"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reviews",
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("reviewed_user_id", sa.Integer(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["client_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["reviewed_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_reviews_id"),
        "reviews",
        ["id"],
        unique=False
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_reviews_id"),
        table_name="reviews"
    )

    op.drop_table("reviews")
