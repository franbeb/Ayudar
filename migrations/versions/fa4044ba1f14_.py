"""empty message

Revision ID: fa4044ba1f14
Revises: 984e2acf68a6
Create Date: 2020-11-03 10:13:34.389694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa4044ba1f14'
down_revision = '984e2acf68a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('centers', sa.Column('gender', sa.Enum('M', 'F'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('centers', 'gender')
    # ### end Alembic commands ###
