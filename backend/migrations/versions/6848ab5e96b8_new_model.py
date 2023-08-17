"""new model

Revision ID: 6848ab5e96b8
Revises: c4d7f9729c0f
Create Date: 2023-08-17 13:37:50.460191

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6848ab5e96b8'
down_revision = 'c4d7f9729c0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('type', sa.String(length=255), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('capacity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rank',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('points_required', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('is_child_rank', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('promotion',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('rank_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['rank_id'], ['rank.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_event',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'event_id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_coach', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('pin', sa.String(length=4), nullable=True))
        batch_op.add_column(sa.Column('start_date', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('last_promotion', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('point_total', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('rank_id', sa.Integer(), nullable=True))
        batch_op.create_unique_constraint(None, ['username'])
        batch_op.create_foreign_key(None, 'rank', ['rank_id'], ['id'])
        batch_op.drop_column('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', mysql.VARCHAR(length=255), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('rank_id')
        batch_op.drop_column('point_total')
        batch_op.drop_column('last_promotion')
        batch_op.drop_column('start_date')
        batch_op.drop_column('pin')
        batch_op.drop_column('is_coach')

    op.drop_table('user_event')
    op.drop_table('promotion')
    op.drop_table('rank')
    op.drop_table('event')
    # ### end Alembic commands ###