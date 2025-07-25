"""added member pic

Revision ID: 30d7da5f3c8a
Revises: 1ed1556f55ed
Create Date: 2025-06-19 10:47:55.439626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30d7da5f3c8a'
down_revision = '1ed1556f55ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('members', schema=None) as batch_op:
        batch_op.add_column(sa.Column('member_pic', sa.String(200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('members', schema=None) as batch_op:
        batch_op.drop_column('member_pic')

    # ### end Alembic commands ###
