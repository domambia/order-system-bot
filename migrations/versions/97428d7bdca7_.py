"""empty message

Revision ID: 97428d7bdca7
Revises: 44dd251e9626
Create Date: 2019-05-17 08:40:32.278912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97428d7bdca7'
down_revision = '44dd251e9626'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('username', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'username')
    # ### end Alembic commands ###