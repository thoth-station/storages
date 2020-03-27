"""Flag for if specific hash has gone missing, defaults to present

Revision ID: ecb0ca258835
Revises: 0ea53ec16d6b
Create Date: 2020-03-26 15:26:00.311857+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecb0ca258835'
down_revision = '0ea53ec16d6b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('python_artifact', sa.Column('present', sa.Boolean(), nullable=False, server_default="false"))


    # NOTE: I am unsure where these came from?
    op.alter_column('python_artifact', 'artifact_hash_sha256',
               existing_type=sa.TEXT(),
               type_=sa.String(length=256),
               existing_nullable=False)
    op.alter_column('python_artifact', 'artifact_name',
               existing_type=sa.TEXT(),
               type_=sa.String(length=256),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('python_artifact', 'artifact_name',
               existing_type=sa.String(length=256),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('python_artifact', 'artifact_hash_sha256',
               existing_type=sa.String(length=256),
               type_=sa.TEXT(),
               existing_nullable=False)
    op.drop_column('python_artifact', 'present')
    # ### end Alembic commands ###
