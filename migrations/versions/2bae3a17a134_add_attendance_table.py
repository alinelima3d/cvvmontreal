"""add attendance table

Revision ID: 2bae3a17a134
Revises: 310328a412b2
Create Date: 2025-07-16 11:00:50.647332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bae3a17a134'
down_revision = '310328a412b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attendance',
    sa.Column('member_id', sa.Integer(), nullable=True),
    sa.Column('meeting_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['meeting_id'], ['meetings.id'], ),
    sa.ForeignKeyConstraint(['member_id'], ['members.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('attendance')
    # ### end Alembic commands ###
