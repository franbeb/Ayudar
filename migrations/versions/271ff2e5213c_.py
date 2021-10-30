"""empty message

Revision ID: 271ff2e5213c
Revises: 6987a3a23685
Create Date: 2020-11-03 16:08:47.681785

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '271ff2e5213c'
down_revision = '6987a3a23685'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tipo_centro',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_tipo_centro_nombre'), 'tipo_centro', ['nombre'], unique=False)
    op.drop_column('centers', 'tipo_centro')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('centers', sa.Column('tipo_centro', mysql.ENUM('1', '2'), nullable=True))
    op.drop_index(op.f('ix_tipo_centro_nombre'), table_name='tipo_centro')
    op.drop_table('tipo_centro')
    # ### end Alembic commands ###