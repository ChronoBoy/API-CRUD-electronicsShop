"""create items table

Revision ID: ed6506eeafd3
Revises: f3d71d6b0351
Create Date: 2021-09-28 09:20:31.454861

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import ForeignKey 




# revision identifiers, used by Alembic.
revision = 'ed6506eeafd3'
down_revision = 'f3d71d6b0351'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'items',
        sa.Column('item_id', sa.Integer, primary_key=True, unique=True),
        sa.Column('item_name', sa.String(100), nullable=False),
        sa.Column('item_description', sa.String(100), nullable=False),
        sa.Column('item_owner', sa.Integer,ForeignKey('users.user_id'))

        
         
    )


def downgrade():
    op.drop_table('items')
