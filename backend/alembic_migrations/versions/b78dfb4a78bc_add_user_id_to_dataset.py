"""Add user_id column to datasets

Revision ID: b78dfb4a78bc_add_user_id_to_dataset
Revises: b78dfb4a78ba
Create Date: 2025-01-14

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b78dfb4a78bc"
down_revision = "b78dfb4a78ba"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("datasets", sa.Column("user_id", sa.Integer(), nullable=True))
    op.execute(
        "UPDATE datasets SET user_id = 1"
    )  # or handle how you wish for existing data
    op.alter_column("datasets", "user_id", nullable=False)
    op.create_foreign_key(
        "fk_datasets_user_id",
        "datasets",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade():
    op.drop_constraint("fk_datasets_user_id", "datasets", type_="foreignkey")
    op.drop_column("datasets", "user_id")
