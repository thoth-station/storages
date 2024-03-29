"""Added entry in KebechetGithubInstallation table for environment name.

Revision ID: 5c1e7425ce60
Revises: 65ae36e5c38a
Create Date: 2021-08-10 15:38:46.589634+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5c1e7425ce60"
down_revision = "65ae36e5c38a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("kebechet_github_installations", sa.Column("runtime_environment_name", sa.Text(), nullable=True))
    op.create_unique_constraint(None, "kebechet_github_installations", ["slug", "runtime_environment_name"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "kebechet_github_installations", type_="unique")
    op.drop_column("kebechet_github_installations", "runtime_environment_name")
    # ### end Alembic commands ###
