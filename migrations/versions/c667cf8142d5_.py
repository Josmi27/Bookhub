"""empty message

Revision ID: c667cf8142d5
Revises: 1dafd9a05a96
Create Date: 2019-04-10 00:31:41.016847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c667cf8142d5'
down_revision = '1dafd9a05a96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recommendation', sa.Column('recommender', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'recommendation', 'user', ['recommender'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'recommendation', type_='foreignkey')
    op.drop_column('recommendation', 'recommender')
    # ### end Alembic commands ###