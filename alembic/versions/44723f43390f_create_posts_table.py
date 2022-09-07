"""create posts table

Revision ID: 44723f43390f
Revises: 
Create Date: 2022-09-07 23:43:17.765182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44723f43390f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String, nullable=False))
    pass
    


def downgrade():
    op.drop_table('posts')
