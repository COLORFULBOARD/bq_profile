from setuptools import find_packages, setup

from bq_profile.__version__ import __version__

setup(
    name="bq_profile",
    version=__version__,
    packages=find_packages(exclude=("tests",)),
    install_requires=[],
    entry_points={"console_scripts": ["bq_profile=bq_profile.bq_profile:main"]},
)
