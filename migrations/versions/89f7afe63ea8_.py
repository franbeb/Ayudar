"""empty message

Revision ID: 89f7afe63ea8
Revises: 6232673ba35f
Create Date: 2020-10-18 22:28:22.068689

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89f7afe63ea8'
down_revision = '6232673ba35f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('active', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('date_created', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('perfil', sa.String(length=40), nullable=True))
    op.add_column('users', sa.Column('username', sa.String(length=30), nullable=False))
    op.create_index(op.f('ix_users_perfil'), 'users', ['perfil'], unique=False)
    op.create_unique_constraint(None, 'users', ['email'])
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_index(op.f('ix_users_perfil'), table_name='users')
    op.drop_column('users', 'username')
    op.drop_column('users', 'perfil')
    op.drop_column('users', 'date_created')
    op.drop_column('users', 'active')
    # ### end Alembic commands ###