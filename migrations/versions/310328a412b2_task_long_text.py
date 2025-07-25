"""task long text

Revision ID: 310328a412b2
Revises: b6a1d1749c2c
Create Date: 2025-07-15 20:02:20.645866

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '310328a412b2'
down_revision = 'b6a1d1749c2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task_repartition_texts', schema=None) as batch_op:
        batch_op.alter_column('text',
               existing_type=mysql.VARCHAR(length=400),
               type_=sa.Text(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task_repartition_texts', schema=None) as batch_op:
        batch_op.alter_column('text',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=400),
               existing_nullable=True)

    # ### end Alembic commands ###
