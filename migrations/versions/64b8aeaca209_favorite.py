"""favorite

Revision ID: 64b8aeaca209
Revises: 1c6e64b3ddd6
Create Date: 2026-03-10 16:16:56.844831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64b8aeaca209'
down_revision = '1c6e64b3ddd6'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    creation_columns = {column['name'] for column in inspector.get_columns('creation')}

    if 'class' in creation_columns:
        with op.batch_alter_table('creation', schema=None) as batch_op:
            batch_op.drop_column('class')


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    creation_columns = {column['name'] for column in inspector.get_columns('creation')}

    if 'class' not in creation_columns:
        with op.batch_alter_table('creation', schema=None) as batch_op:
            batch_op.add_column(sa.Column('class', sa.TEXT(), nullable=True))
