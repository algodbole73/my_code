"""add_content_columns

Revision ID: cae0b388105a
Revises: 547b08eda099
Create Date: 2022-11-26 08:40:35.427886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cae0b388105a'
down_revision = '547b08eda099'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(), nullable=False) )
    pass


def downgrade():
    op.drop_column('posts','contnet')
    pass
