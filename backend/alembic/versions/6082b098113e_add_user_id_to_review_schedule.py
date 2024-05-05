"""add user id to review schedule

Revision ID: 6082b098113e
Revises: 2982f9eb827d
Create Date: 2024-05-05 16:47:07.479180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6082b098113e'
down_revision: Union[str, None] = '2982f9eb827d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('review_schedules', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'review_schedules', 'cards', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'review_schedules', type_='foreignkey')
    op.drop_column('review_schedules', 'user_id')
    # ### end Alembic commands ###
