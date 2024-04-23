"""all new 3

Revision ID: 562b0a887d01
Revises: 55a732d177ba
Create Date: 2024-04-22 18:29:48.165935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '562b0a887d01'
down_revision = '55a732d177ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'product', ['product_id'], ['id'])
        batch_op.drop_column('number')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.add_column(sa.Column('number', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('quantity')

    # ### end Alembic commands ###
