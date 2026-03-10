from alembic import op
# use flask db upgrade to get the update
def upgrade():
    op.execute(
        "INSERT INTO tool (id, name) VALUES (4, 'Mixed Media')"
    )