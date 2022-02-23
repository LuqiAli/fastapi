"""create posts table

Revision ID: 294f8938a6bc
Revises: 
Create Date: 2022-02-23 12:34:10.549561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '294f8938a6bc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
