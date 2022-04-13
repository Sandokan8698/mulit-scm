# Copyright (c) 2022 Shutterfly. All rights reserved.
"""
Setuptools build script
"""
from setuptools import find_packages
from setuptools import setup

setup(
    name="sfly.ppt.environment.cleaner_service",
    description="Environment Cleaner Service",
    author="Denys Mendez",
    author_email="v-denys.mendez@shutterfly.com",
    url=("https://gh.internal.shutterfly.com/shutterfly/"
         "ppt-environment-cleaner-service"),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    namespace_packages=[
        'sfly',
        'sfly.ppt',
        'sfly.ppt.environment',
        'sfly.ppt.environment.cleaner_service'
    ],
    setup_requires=[
        'setuptools_scm==3.3.5a1',
        'pytest-runner'
    ],
    tests_require=[
        'coverage>=4.5.1',
        'pytest>=3.4.2',
        'pytest-cov>=2.5.1',
        'pytest-html>=1.16.1',
        'pytest-runner>=4.2',
        'pytest-sugar>=0.3.3',
        'moto>=1.3.13',
        'pytest-env>=0.6.2',
        'mock>=3.0.5',
        'testcontainers[postgresql]>=2.5'
    ],
    install_requires=[
        "boto3",
        "botocore",
        "boto3",
        "psycopg2>=2.8.4",
        "SQLAlchemy==1.3.12"
    ],
    use_scm_version={
        'write_to': 'version.py',
        'fallback_version': '1.2.3'
    }
)
