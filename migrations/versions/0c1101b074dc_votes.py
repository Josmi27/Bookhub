"""votes

Revision ID: 0c1101b074dc
Revises: b0d3f8a7bbf2
Create Date: 2019-04-22 23:44:10.129105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c1101b074dc'
down_revision = 'b0d3f8a7bbf2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('upvote_id', sa.Integer(), nullable=True),
    sa.Column('downvote_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['downvote_id'], ['recommendation.book_title'], ),
    sa.ForeignKeyConstraint(['upvote_id'], ['recommendation.book_title'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###