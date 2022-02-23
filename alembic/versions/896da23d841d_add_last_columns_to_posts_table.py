"""add last columns to posts table

Revision ID: 896da23d841d
Revises: f52accb99931
Create Date: 2022-02-23 12:58:42.899596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '896da23d841d'
down_revision = 'f52accb99931'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(), nullable=False, server_default='True'),)
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
