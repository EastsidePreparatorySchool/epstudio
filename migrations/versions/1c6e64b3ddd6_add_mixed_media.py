"""add_mixed_media

Revision ID: 1c6e64b3ddd6
Revises: 85badb76fef7
Create Date: 2026-03-10 16:12:28.613191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c6e64b3ddd6'
down_revision = '85badb76fef7'
branch_labels = None
depends_on = None

# use flask db upgrade to get the update
def upgrade():
    bind = op.get_bind()
    existing_tool = bind.execute(
        sa.text("SELECT id FROM tool WHERE id = :id OR name = :name"),
        {"id": 4, "name": "Mixed Media"}
    ).fetchone()

    if existing_tool is None:
        bind.execute(
            sa.text("INSERT INTO tool (id, name) VALUES (:id, :name)"),
            {"id": 4, "name": "Mixed Media"}
        )


def downgrade():
    bind = op.get_bind()
    bind.execute(
        sa.text("DELETE FROM tool WHERE id = :id AND name = :name"),
        {"id": 4, "name": "Mixed Media"}
    )
