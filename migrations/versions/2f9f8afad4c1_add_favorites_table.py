"""add favorites table

Revision ID: 2f9f8afad4c1
Revises: 64b8aeaca209
Create Date: 2026-03-17 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f9f8afad4c1'
down_revision = '64b8aeaca209'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'favorites',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('creation_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['creation_id'], ['creation.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('user_id', 'creation_id')
    )


def downgrade():
    op.drop_table('favorites')
