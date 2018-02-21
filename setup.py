from setuptools import setup


def get_install_requires():
    with open('requirements.txt', 'r') as requirements_file:
        return requirements_file.read().splitlines()


setup(
    name='thoth-storages',
    version='0.0.0',
    description='Storage and database adapters available in project Thoth',
    long_description='Storage and database adapters available in project Thoth',
    author='Fridolin Pokorny',
    author_email='fridolin@redhat.com',
    license='GPLv2+',
    packages=['thoth.storages'],
    zip_safe=False,
    install_requires=get_install_requires()
)
