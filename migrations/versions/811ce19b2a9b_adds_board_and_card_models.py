"""adds Board and Card models

Revision ID: 811ce19b2a9b
Revises: 
Create Date: 2023-06-26 13:44:24.146895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '811ce19b2a9b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('board',
    sa.Column('board_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('owner', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('board_id')
    )
    op.create_table('card',
    sa.Column('card_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('likes_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('card_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('card')
    op.drop_table('board')
    # ### end Alembic commands ###
