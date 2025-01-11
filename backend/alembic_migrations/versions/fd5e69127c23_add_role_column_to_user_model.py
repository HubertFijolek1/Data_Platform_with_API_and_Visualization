"""Add role column to User model

Revision ID: fd5e69127c23
Revises: 62472d9a96f9
Create Date: 2025-01-04 09:19:39.443294

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fd5e69127c23"
down_revision: Union[str, None] = "62472d9a96f9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("role", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "role")
    # ### end Alembic commands ###
