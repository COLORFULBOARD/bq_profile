from setuptools import find_packages, setup

from bq_profile.__version__ import __version__

setup(
    name="bq_profile",
    version=__version__,
    packages=find_packages(exclude=("tests",)),
    install_requires=[
        "pandas==0.25.3",
        "pandas-gbq==0.13.0",
        "pandas-profiling==2.4.0",
        "google-cloud-bigquery==1.23.1",
        "google-cloud-storage==1.25.0",
    ],
    entry_points={"console_scripts": ["bq_profile=bq_profile.bq_profile:main"]},
)
