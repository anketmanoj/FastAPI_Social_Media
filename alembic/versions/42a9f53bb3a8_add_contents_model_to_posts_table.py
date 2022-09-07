"""add contents model to posts table

Revision ID: 42a9f53bb3a8
Revises: 44723f43390f
Create Date: 2022-09-07 23:51:10.456685

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42a9f53bb3a8'
down_revision = '44723f43390f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
