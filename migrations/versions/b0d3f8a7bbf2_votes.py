"""votes

Revision ID: b0d3f8a7bbf2
Revises: 2440d94fbc42
Create Date: 2019-04-22 22:17:12.904965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0d3f8a7bbf2'
down_revision = '2440d94fbc42'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('upvote_id', sa.Integer(), nullable=True),
    sa.Column('downvote_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['downvote_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['upvote_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###
