import os
from setuptools import setup


def get_install_requires():
    with open('requirements.txt', 'r') as requirements_file:
        # TODO: respect hashes in requirements.txt file
        res = requirements_file.readlines()
        return [req.split(' ', maxsplit=1)[0] for req in res if req]


def get_version():
    with open(os.path.join('thoth', 'storages', '__init__.py')) as f:
        content = f.readlines()

    for line in content:
        if line.startswith('__version__ ='):
            # dirty, remove trailing and leading chars
            return line.split(' = ')[1][1:-2]
    raise ValueError("No version identifier found")


setup(
    name='thoth-storages',
    version=get_version(),
    description='Storage and database adapters available in project Thoth',
    long_description='Storage and database adapters available in project Thoth',
    author='Fridolin Pokorny',
    author_email='fridolin@redhat.com',
    license='GPLv2+',
    packages=[
        'thoth.storages',
        'thoth.storages.graph'
    ],
    zip_safe=False,
    install_requires=get_install_requires()
)
