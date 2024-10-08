"""initial migration

Revision ID: a602a2876f5d
Revises: 
Create Date: 2024-10-02 13:01:06.038272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a602a2876f5d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('notifications', sa.Boolean(), nullable=True),
    sa.Column('light_mode', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tool',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=150), nullable=False),
    sa.Column('last_name', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('gradyear', sa.Integer(), nullable=True),
    sa.Column('settings_id', sa.Integer(), nullable=True),
    sa.Column('pfp_path', sa.String(length=200), nullable=True),
    sa.Column('pronouns', sa.String(length=50), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['settings_id'], ['settings.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('creation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('photo_path', sa.String(length=200), nullable=True),
    sa.Column('video_path', sa.String(length=200), nullable=True),
    sa.Column('caption', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('creations_tools',
    sa.Column('creation_id', sa.Integer(), nullable=False),
    sa.Column('tool_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['creation_id'], ['creation.id'], ),
    sa.ForeignKeyConstraint(['tool_id'], ['tool.id'], ),
    sa.PrimaryKeyConstraint('creation_id', 'tool_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('creations_tools')
    op.drop_table('creation')
    op.drop_table('users')
    op.drop_table('tool')
    op.drop_table('settings')
    # ### end Alembic commands ###
