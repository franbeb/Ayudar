"""empty message

Revision ID: a54c5808ef06
Revises: bd75febd8c08
Create Date: 2020-12-10 19:53:38.427901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a54c5808ef06'
down_revision = 'bd75febd8c08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('turns', sa.Column('name', sa.String(length=30), nullable=True))
    op.add_column('turns', sa.Column('surname', sa.String(length=30), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('turns', 'surname')
    op.drop_column('turns', 'name')
    # ### end Alembic commands ###