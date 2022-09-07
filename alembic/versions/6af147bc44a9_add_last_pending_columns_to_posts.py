"""add last pending columns to posts

Revision ID: 6af147bc44a9
Revises: 97c29aab1ded
Create Date: 2022-09-08 00:09:09.464862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6af147bc44a9'
down_revision = '97c29aab1ded'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(),server_default='TRUE', nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
