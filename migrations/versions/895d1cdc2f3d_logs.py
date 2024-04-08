"""logs

Revision ID: 895d1cdc2f3d
Revises: 1dc00b6b9ac5
Create Date: 2024-04-06 03:39:09.285423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '895d1cdc2f3d'
down_revision = '1dc00b6b9ac5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('log_date', sa.Date(), nullable=True),
    sa.Column('log_time', sa.Time(), nullable=True),
    sa.Column('log_text', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('log')
    op.drop_table('contents')
    # ### end Alembic commands ###
