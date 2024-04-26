"""777

Revision ID: 0e6af32115e3
Revises: 
Create Date: 2024-04-26 21:35:22.686167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e6af32115e3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('author', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=50),
               nullable=True)
        batch_op.alter_column('desc',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=200),
               existing_nullable=True)

    with op.batch_alter_table('new', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', sa.Integer(), nullable=True))
        batch_op.drop_constraint('new_author_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'author', ['author'], ['id'])
        batch_op.drop_column('author_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('new', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('new_author_id_fkey', 'author', ['author_id'], ['id'])
        batch_op.drop_column('author')

    with op.batch_alter_table('author', schema=None) as batch_op:
        batch_op.alter_column('desc',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=100),
               nullable=False)

    # ### end Alembic commands ###
