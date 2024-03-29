"""Add CVE link to CVE table

Revision ID: 92a5e912f877
Revises: 0165f03250a6
Create Date: 2021-10-26 12:22:27.972582+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "92a5e912f877"
down_revision = "0165f03250a6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("cve", sa.Column("link", sa.Text(), nullable=True))
    # Let's drop all the CVE information so that the new gets filled properly.
    op.execute("DELETE FROM CVE")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("cve", "link")
    # ### end Alembic commands ###
