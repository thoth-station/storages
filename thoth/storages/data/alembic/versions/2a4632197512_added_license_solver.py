"""added license-solver

Revision ID: 2a4632197512
Revises: 2b787ddad4a4
Create Date: 2022-06-09 07:26:05.576715+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2a4632197512"
down_revision = "2b787ddad4a4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "python_package_license",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("license_name", sa.Text(), nullable=False),
        sa.Column("license_identifier", sa.Text(), nullable=False),
        sa.Column("license_version", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.add_column("python_package_version", sa.Column("package_license", sa.Integer(), nullable=True))
    op.add_column("python_package_version", sa.Column("package_license_warning", sa.Boolean(), nullable=True))
    op.create_foreign_key("fk_license", "python_package_version", "python_package_license", ["package_license"], ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("fk_license", "python_package_version", type_="foreignkey")
    op.drop_column("python_package_version", "package_license_warning")
    op.drop_column("python_package_version", "package_license")
    op.drop_table("python_package_license")
    # ### end Alembic commands ###
