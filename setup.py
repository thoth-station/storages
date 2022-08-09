"""Setup configuration for storages module."""

import os
import sys
from functools import partial
from setuptools import setup
from setuptools.command.test import test
from pathlib import Path


def _get_requires(requirements: str):
    """Get requirements for storages module."""
    with open(requirements, "r") as requirements_file:
        # TODO: respect hashes in requirements.txt file
        res = requirements_file.readlines()
        return [req.split(" ", maxsplit=1)[0] for req in res if req]


get_install_requires = partial(_get_requires, "requirements.txt")

get_test_requires = partial(_get_requires, "requirements-test.txt")


def get_version():
    """Get current version of storages module."""
    with open(os.path.join("thoth", "storages", "__init__.py")) as f:
        content = f.readlines()

    for line in content:
        if line.startswith("__version__ ="):
            # dirty, remove trailing and leading chars
            return line.split(" = ")[1][1:-2]
    raise ValueError("No version identifier found")


class Test(test):
    """Introduce test command to run testsuite using pytest."""

    _IMPLICIT_PYTEST_ARGS = [
        "tests/",
        "--timeout=2",
        "--cov=./thoth",
        # '--mypy',
        "thoth/",
        "--capture=no",
        "--verbose",
        "-l",
        "-s",
        "-vv",
    ]

    user_options = [("pytest-args=", "a", "Arguments to pass into py.test")]

    def initialize_options(self):
        """Initialize cli options."""
        super().initialize_options()
        self.pytest_args = None

    def finalize_options(self):
        """Finalize cli options."""
        super().finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """Run module tests."""
        import pytest

        passed_args = list(self._IMPLICIT_PYTEST_ARGS)

        if self.pytest_args:
            self.pytest_args = [arg for arg in self.pytest_args.split() if arg]
            passed_args.extend(self.pytest_args)

        sys.exit(pytest.main(passed_args))


VERSION = get_version()
setup(
    name="thoth-storages",
    version=VERSION,
    description="Storage and database adapters available in project Thoth",
    long_description=Path("README.rst").read_text(),
    long_description_content_type="text/x-rst",
    author="Fridolin Pokorny",
    author_email="fridolin@redhat.com",
    license="GPLv3+",
    packages=["thoth.storages", "thoth.storages.graph"],
    package_data={
        "thoth.storages": [
            "py.typed",
            os.path.join("data", "alembic.ini"),
            os.path.join("data", "alembic", "script.py.mako"),
            os.path.join("data", "alembic", "env.py"),
            os.path.join("data", "alembic", "versions", "*.py"),
        ]
    },
    zip_safe=False,
    install_requires=get_install_requires(),
    tests_require=get_test_requires(),
    cmdclass={"test": Test},
    entry_points={"console_scripts": ["thoth-storages=thoth.storages.cli:cli"]},
    url="https://github.com/thoth-station/storages",
    maintainer="Francesco Murdaca",
    maintainer_email="fmurdaca@redhat.com",
    command_options={
        "build_sphinx": {
            "version": ("setup.py", VERSION),
            "release": ("setup.py", VERSION),
        }
    },
)
