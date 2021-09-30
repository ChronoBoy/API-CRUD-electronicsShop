"""create user table

Revision ID: f3d71d6b0351
Revises: 
Create Date: 2021-09-28 09:17:46.492309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3d71d6b0351'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
        op.create_table(
        'users',
        sa.Column('user_id', sa.Integer, primary_key=True, unique=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('lastname', sa.String(100), nullable=False),
        sa.Column('age', sa.Integer),
        sa.Column('email', sa.String(100), nullable=False, unique=True),
        sa.Column('password', sa.String(30), nullable=False),
        sa.Column('is_active', sa.Boolean, default=True)

    )


def downgrade():
    op.drop_table('users')
