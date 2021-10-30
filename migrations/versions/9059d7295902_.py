"""empty message

Revision ID: 9059d7295902
Revises: 8478f31485e6
Create Date: 2020-11-03 11:38:53.481804

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9059d7295902'
down_revision = '8478f31485e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('id', table_name='municipios')
    op.drop_index('ix_municipios_nombre', table_name='municipios')
    op.drop_table('municipios')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('municipios',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('nombre', mysql.VARCHAR(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_municipios_nombre', 'municipios', ['nombre'], unique=False)
    op.create_index('id', 'municipios', ['id'], unique=True)
    # ### end Alembic commands ###