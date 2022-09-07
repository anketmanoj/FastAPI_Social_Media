"""add foreign key to post table

Revision ID: 97c29aab1ded
Revises: dcfcf3ca79ae
Create Date: 2022-09-08 00:03:48.770569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97c29aab1ded'
down_revision = 'dcfcf3ca79ae'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE", onupdate="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
