"""Initial migration.

Revision ID: 3d822eec798b
Revises: 
Create Date: 2021-01-31 14:18:17.258864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d822eec798b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classroom',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=False),
    sa.Column('time', sa.Time(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('volunteer_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('profile_link', sa.String(length=120), nullable=False),
    sa.Column('seeking_volunteer', sa.Boolean(), nullable=False),
    sa.Column('seeking_description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('volunteer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('profile_link', sa.String(length=120), nullable=False),
    sa.Column('seeking_student', sa.Boolean(), nullable=False),
    sa.Column('seeking_description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student_classroom',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('classroom_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['classroom_id'], ['classroom.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('student_id', 'classroom_id')
    )
    op.create_table('volunteer_classroom',
    sa.Column('volunteer_id', sa.Integer(), nullable=False),
    sa.Column('classroom_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['classroom_id'], ['classroom.id'], ),
    sa.ForeignKeyConstraint(['volunteer_id'], ['volunteer.id'], ),
    sa.PrimaryKeyConstraint('volunteer_id', 'classroom_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('volunteer_classroom')
    op.drop_table('student_classroom')
    op.drop_table('volunteer')
    op.drop_table('student')
    op.drop_table('classroom')
    # ### end Alembic commands ###