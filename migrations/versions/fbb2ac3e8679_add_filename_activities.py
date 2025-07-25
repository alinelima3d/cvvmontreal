"""add filename activities

Revision ID: fbb2ac3e8679
Revises: 7880b97a2801
Create Date: 2025-07-15 12:25:19.549960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbb2ac3e8679'
down_revision = '7880b97a2801'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('activities', schema=None) as batch_op:
        batch_op.add_column(sa.Column('filename', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('activities', schema=None) as batch_op:
        batch_op.drop_column('filename')

    # ### end Alembic commands ###
