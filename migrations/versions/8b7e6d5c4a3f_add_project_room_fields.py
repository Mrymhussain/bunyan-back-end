"""add project room fields

Revision ID: 8b7e6d5c4a3f
Revises: def74528d13e
Create Date: 2026-10-07
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8b7e6d5c4a3f"
down_revision: Union[str, None] = "def74528d13e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "projects",
        sa.Column("meeting_title", sa.String(), nullable=True),
    )

    op.add_column(
        "projects",
        sa.Column("meeting_at", sa.DateTime(), nullable=True),
    )

    op.add_column(
        "projects",
        sa.Column("meeting_type", sa.String(), nullable=True),
    )

    op.add_column(
        "projects",
        sa.Column("meeting_link", sa.String(), nullable=True),
    )

    op.add_column(
        "project_members",
        sa.Column(
            "approved",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )

    op.add_column(
        "project_members",
        sa.Column("approval_note", sa.Text(), nullable=True),
    )

    op.alter_column(
        "project_members",
        "approved",
        server_default=None,
    )

    op.create_table(
        "project_updates",
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_project_updates_id"),
        "project_updates",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_project_updates_id"),
        table_name="project_updates",
    )

    op.drop_table("project_updates")

    op.drop_column(
        "project_members",
        "approval_note",
    )

    op.drop_column(
        "project_members",
        "approved",
    )

    op.drop_column(
        "projects",
        "meeting_link",
    )

    op.drop_column(
        "projects",
        "meeting_type",
    )

    op.drop_column(
        "projects",
        "meeting_at",
    )

    op.drop_column(
        "projects",
        "meeting_title",
    )
