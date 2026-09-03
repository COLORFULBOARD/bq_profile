from setuptools import find_packages, setup

from bq_profile.__version__ import __version__

setup(
    name="bq_profile",
    version=__version__,
    packages=find_packages(exclude=("tests",)),
    install_requires=[
        "pandas==2.3.3",
        "pandas-gbq==0.35.2",
        "google-cloud-bigquery==3.44.0",
        "google-cloud-storage==3.13.1",
    ],
    entry_points={"console_scripts": ["bq_profile=bq_profile.bq_profile:main"]},
)
