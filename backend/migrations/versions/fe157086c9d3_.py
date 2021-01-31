"""empty message

Revision ID: fe157086c9d3
Revises: 3d822eec798b
Create Date: 2021-01-31 14:27:25.943997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe157086c9d3'
down_revision = '3d822eec798b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('gender', sa.String(length=10), nullable=True))
    op.add_column('volunteer', sa.Column('gender', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('volunteer', 'gender')
    op.drop_column('student', 'gender')
    # ### end Alembic commands ###
