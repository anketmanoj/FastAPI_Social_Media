"""add users table

Revision ID: dcfcf3ca79ae
Revises: 42a9f53bb3a8
Create Date: 2022-09-07 23:55:36.500345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcfcf3ca79ae'
down_revision = '42a9f53bb3a8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
