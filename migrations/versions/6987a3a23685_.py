"""empty message

Revision ID: 6987a3a23685
Revises: 404a769295e5
Create Date: 2020-11-03 13:58:34.065372

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6987a3a23685'
down_revision = '404a769295e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('centers', sa.Column('hora_apertura', mysql.TIME(), nullable=False))
    op.add_column('centers', sa.Column('hora_cierre', mysql.TIME(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('centers', 'hora_cierre')
    op.drop_column('centers', 'hora_apertura')
    # ### end Alembic commands ###
