"""create freebies table

Revision ID: 79c90410b731
Revises: 455a18c70ed5
Create Date: 2025-05-26 10:59:51.427528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79c90410b731'
down_revision: Union[str, None] = '455a18c70ed5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('freebies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('item_name', sa.String(), nullable=True),
        sa.Column('value', sa.Integer(), nullable=True),
        sa.Column('dev_id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['dev_id'], ['devs.id'], name='fk_freebies_dev_id_devs'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name='fk_freebies_company_id_companies'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('freebies')
