"""added thoth-license-solver

Revision ID: 481cc459643b
Revises: 2b787ddad4a4
Create Date: 2022-04-29 13:25:32.155199+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '481cc459643b'
down_revision = '2b787ddad4a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
    	'python_package_license',
	sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
	sa.Column('license_name', sa.Text(), nullable=False),
	sa.Column('license_identifier', sa.Text(), nullable=False),
	sa.Column('license_version', sa.Text(), nullable=False),
	sa.PrimaryKeyConstraint('id')
    )

    op.add_column('python_package_version', sa.Column('package_license', sa.Integer(), nullable=True))
    op.add_column('python_package_version', sa.Column('package_license_warning', sa.Boolean(), nullable=True))
    
    op.create_foreign_key(None, 'python_package_version', 'python_package_license', ['package_license'], ['id'])
    
    
#    op.create_unique_constraint(None, 'python_package_version_entity_rule', ['id'])
#    op.drop_index('thoth_s2i_image_name', table_name='software_environment')
#    op.create_index('thoth_image_name', 'software_environment', ['thoth_image_version'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
#    op.drop_index('thoth_image_name', table_name='software_environment')
#    op.create_index('thoth_s2i_image_name', 'software_environment', ['thoth_image_version'], unique=False)
#    op.drop_constraint(None, 'python_package_version_entity_rule', type_='unique')
#    op.drop_constraint(None, 'python_package_version', type_='foreignkey')
    op.drop_column('python_package_version', 'package_license_warning')
    op.drop_column('python_package_version', 'package_license')
   # op.alter_column('has_symbol', 'versioned_symbol_id',
   #            existing_type=sa.INTEGER(),
   #            nullable=True)
   # op.alter_column('has_symbol', 'software_environment_id',
   #            existing_type=sa.INTEGER(),
   #            nullable=True)
    op.drop_table('python_package_license')
    # ### end Alembic commands ###
