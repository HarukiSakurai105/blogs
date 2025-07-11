"""add is_edited and edited_at to Post

Revision ID: 49ea0d87f875
Revises: d91690dbeac5
Create Date: 2025-06-18 16:02:58.175091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49ea0d87f875'
down_revision = 'd91690dbeac5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_edited', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('edited_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('edited_at')
        batch_op.drop_column('is_edited')

    # ### end Alembic commands ###
