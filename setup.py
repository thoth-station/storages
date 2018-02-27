from setuptools import setup


def get_install_requires():
    with open('requirements.txt', 'r') as requirements_file:
        # TODO: respect hashes in requirements.txt file
        res = requirements_file.readlines()
        return [req.split(' ', maxsplit=1)[0] for req in res if req]


setup(
    name='thoth-storages',
    version='0.0.2',
    description='Storage and database adapters available in project Thoth',
    long_description='Storage and database adapters available in project Thoth',
    author='Fridolin Pokorny',
    author_email='fridolin@redhat.com',
    license='GPLv2+',
    packages=[
        'thoth.storages',
        'thoth.storages.janusgraph'
    ],
    zip_safe=False,
    install_requires=get_install_requires()
)
