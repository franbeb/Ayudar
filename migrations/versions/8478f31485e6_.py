"""empty message

Revision ID: 8478f31485e6
Revises: 5c71a59fe470
Create Date: 2020-11-03 11:10:44.553802

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8478f31485e6'
down_revision = '5c71a59fe470'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('center_has_municipio')
    op.add_column('centers', sa.Column('municipio', sa.Integer(), nullable=False))
    op.alter_column('centers', 'tipo_centro',
               existing_type=mysql.ENUM('1', '2'),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('centers', 'tipo_centro',
               existing_type=mysql.ENUM('1', '2'),
               nullable=True)
    op.drop_column('centers', 'municipio')
    op.create_table('center_has_municipio',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('center_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('municipio_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['center_id'], ['centers.id'], name='center_has_municipio_ibfk_1'),
    sa.ForeignKeyConstraint(['municipio_id'], ['municipios.id'], name='center_has_municipio_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
