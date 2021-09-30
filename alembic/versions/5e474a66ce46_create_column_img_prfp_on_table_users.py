"""create column img_prf  on table users

Revision ID: 5e474a66ce46
Revises: ed6506eeafd3
Create Date: 2021-09-28 10:07:31.921072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e474a66ce46'
down_revision = 'ed6506eeafd3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('img_prf', sa.String(100)))


def downgrade():
    op.drop_column('img_prf')
