#!/usr/bin/env python

import sys, os

sys.path[:0] = [
    os.path.dirname(__file__),
]

from poolMan import PACKAGE_NAME, PACKAGE_VERSION
from setuptools import setup

setup(
    name=PACKAGE_NAME,
    version="{}".format(PACKAGE_VERSION),
    description="Cluster Pool Supervisor",
    author='Damion K. Wilson',
    include_package_data=True,
    platforms='any',

    install_requires=[
        "tornado",
    ],

    packages = [
        PACKAGE_NAME,
        "{}.reactors".format(PACKAGE_NAME),
        "{}.entry_points".format(PACKAGE_NAME),
    ],

    package_data={
        '': ['examples/*'],
    },

    entry_points = {
        'console_scripts': [
            "pool_console = {}.entry_points:console_session".format(PACKAGE_NAME),
            "pool_service = {}.entry_points:run_cluster".format(PACKAGE_NAME),
        ]
    },
)
