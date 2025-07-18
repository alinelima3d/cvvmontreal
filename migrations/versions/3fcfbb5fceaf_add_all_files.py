"""add all files

Revision ID: 3fcfbb5fceaf
Revises: 30d7da5f3c8a
Create Date: 2025-06-19 11:25:14.464171

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3fcfbb5fceaf'
down_revision = '30d7da5f3c8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('executive_members', schema=None) as batch_op:
        batch_op.add_column(sa.Column('executive_member_pic', sa.String(length=400), nullable=True))

    with op.batch_alter_table('meetings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file', sa.String(length=400), nullable=True))

    with op.batch_alter_table('members', schema=None) as batch_op:
        batch_op.alter_column('member_pic',
               existing_type=mysql.VARCHAR(length=200),
               type_=sa.String(length=400),
               existing_nullable=True)

    with op.batch_alter_table('memberships', schema=None) as batch_op:
        batch_op.add_column(sa.Column('remembered', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('file', sa.String(length=400), nullable=True))
        batch_op.drop_column('warned')

    with op.batch_alter_table('surveys', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file', sa.String(length=400), nullable=True))
        batch_op.alter_column('start',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=True)
        batch_op.alter_column('end',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('surveys', schema=None) as batch_op:
        batch_op.alter_column('end',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=True)
        batch_op.alter_column('start',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=True)
        batch_op.drop_column('file')

    with op.batch_alter_table('memberships', schema=None) as batch_op:
        batch_op.add_column(sa.Column('warned', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('file')
        batch_op.drop_column('remembered')

    with op.batch_alter_table('members', schema=None) as batch_op:
        batch_op.alter_column('member_pic',
               existing_type=sa.String(length=400),
               type_=mysql.VARCHAR(length=200),
               existing_nullable=True)

    with op.batch_alter_table('meetings', schema=None) as batch_op:
        batch_op.drop_column('file')

    with op.batch_alter_table('executive_members', schema=None) as batch_op:
        batch_op.drop_column('executive_member_pic')

    # ### end Alembic commands ###
