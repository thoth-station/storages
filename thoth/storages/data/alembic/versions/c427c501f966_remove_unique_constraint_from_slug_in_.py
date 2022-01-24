"""remove unique constraint from slug in KebechetGithubAppInstallation

Revision ID: c427c501f966
Revises: b718c0f8bc53
Create Date: 2022-01-17 21:26:14.926834+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c427c501f966"
down_revision = "b718c0f8bc53"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("kebechet_github_installations_slug_key", "kebechet_github_installations", type_="unique")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("kebechet_github_installations_slug_key", "kebechet_github_installations", ["slug"])
    # ### end Alembic commands ###