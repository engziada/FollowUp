"""socialaccount

Revision ID: 82cea1a34686
Revises: 39cfd8f7e467
Create Date: 2024-04-03 02:54:28.995461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82cea1a34686'
down_revision = '39cfd8f7e467'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scanlogs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_picture', sa.String(), nullable=True))
        batch_op.drop_column('profile_picture_link')

    with op.batch_alter_table('subprofiles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_picture', sa.String(), nullable=True))
        batch_op.drop_column('profile_picture_link')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subprofiles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_picture_link', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_column('profile_picture')

    with op.batch_alter_table('scanlogs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_picture_link', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_column('profile_picture')

    # ### end Alembic commands ###
