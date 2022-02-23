"""add content column to post

Revision ID: 7eb76e7422d9
Revises: 294f8938a6bc
Create Date: 2022-02-23 12:41:57.986561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7eb76e7422d9'
down_revision = '294f8938a6bc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
