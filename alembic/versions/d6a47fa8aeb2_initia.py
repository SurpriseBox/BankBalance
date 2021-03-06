"""initia

Revision ID: d6a47fa8aeb2
Revises: 
Create Date: 2022-04-14 18:02:39.731010

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'd6a47fa8aeb2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=200), nullable=False),
    sa.Column('last_name', sa.String(length=200), nullable=False),
    sa.Column('patr_name', sa.String(length=200), nullable=False),
    sa.Column('balance', sa.DECIMAL(precision=14, scale=4), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('operation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('type', sa.Enum('withdrawal', 'accrual', 'transaction', name='operationtype'), nullable=True),
    sa.Column('user_from_id', sa.Integer(), nullable=True),
    sa.Column('user_to_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('comment', sa.String(length=500), nullable=False),
    sa.Column('status', sa.Enum('created', 'pending', 'in_progress', 'success', 'error', name='operationstatus'), nullable=False),
    sa.ForeignKeyConstraint(['user_from_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_to_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('operation')
    op.drop_table('user')
    # ### end Alembic commands ###
