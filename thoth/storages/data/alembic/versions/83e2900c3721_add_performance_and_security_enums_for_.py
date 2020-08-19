"""Add performance and security enums for recommendation types

Revision ID: 83e2900c3721
Revises: d6d0b20ec650
Create Date: 2020-08-19 06:49:24.347264+00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '83e2900c3721'
down_revision = 'd6d0b20ec650'
branch_labels = None
depends_on = None

# Solution based on https://stackoverflow.com/a/33617845

name = 'recommendation_type'
tmp_name = 'tmp_' + name

old_options = ('STABLE', 'TESTING', 'LATEST')
new_options = sorted(old_options + ('PERFORMANCE', 'SECURITY'))

new_type = sa.Enum(*new_options, name=name)
old_type = sa.Enum(*old_options, name=name)

tcr = sa.sql.table('adviser_run',
                   sa.Column('recommendation_type', new_type, nullable=False))

def upgrade():
    op.execute('ALTER TYPE ' + name + ' RENAME TO ' + tmp_name)

    new_type.create(op.get_bind())
    op.execute('ALTER TABLE adviser_run ALTER COLUMN recommendation_type ' +
               'TYPE ' + name + ' USING recommendation_type::text::' + name)
    op.execute('DROP TYPE ' + tmp_name)


def downgrade():
    # Convert 'performance' recommendation type into 'stable'                                                                                                                      
    # Convert 'security' recommendation type into 'stable'                                                                                                                      
    op.execute(tcr.update().where(tcr.c.recommendation_type=='PERFORMANCE')
               .values(recommendation_type='STABLE'))
    op.execute(tcr.update().where(tcr.c.recommendation_type=='SECURITY')
               .values(recommendation_type='STABLE'))

    op.execute('ALTER TYPE ' + name + ' RENAME TO ' + tmp_name)

    old_type.create(op.get_bind())
    op.execute('ALTER TABLE adviser_run ALTER COLUMN recommendation_type ' +
               'TYPE ' + name + ' USING recommendation_type::text::' + name)
    op.execute('DROP TYPE ' + tmp_name)
