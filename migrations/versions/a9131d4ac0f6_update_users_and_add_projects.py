"""update Users and add Projects

Revision ID: a9131d4ac0f6
Revises: e27ada9e54b2
Create Date: 2023-09-23 22:24:41.699272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9131d4ac0f6'
down_revision = 'e27ada9e54b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('address', sa.String(length=64), nullable=True),
    sa.Column('creator', sa.Integer(), nullable=True),
    sa.Column('editors', sa.JSON(), nullable=True),
    sa.Column('viewers', sa.JSON(), nullable=True),
    sa.Column('works', sa.JSON(), nullable=True),
    sa.Column('resources', sa.JSON(), nullable=True),
    sa.Column('payments', sa.JSON(), nullable=True),
    sa.Column('dependences', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_project_creator'), ['creator'], unique=False)
        batch_op.create_index(batch_op.f('ix_project_id'), ['id'], unique=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('uuid', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('info', sa.String(length=256), nullable=True))
        batch_op.add_column(sa.Column('created_projects', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('other_projects', sa.JSON(), nullable=True))
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=128),
               existing_nullable=True)
        batch_op.drop_index('ix_user_username')
        batch_op.create_index(batch_op.f('ix_user_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_uuid'), ['uuid'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_uuid'))
        batch_op.drop_index(batch_op.f('ix_user_id'))
        batch_op.create_index('ix_user_username', ['username'], unique=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=120),
               existing_nullable=True)
        batch_op.drop_column('other_projects')
        batch_op.drop_column('created_projects')
        batch_op.drop_column('info')
        batch_op.drop_column('uuid')

    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_project_id'))
        batch_op.drop_index(batch_op.f('ix_project_creator'))

    op.drop_table('project')
    # ### end Alembic commands ###
