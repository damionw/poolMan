#!/usr/bin/env python

import sys

sys.path[:0] = ["./"]

from poolMan import PACKAGE_NAME, PACKAGE_VERSION
from setuptools import setup

setup(
    name=PACKAGE_NAME,
    version="{}".format(PACKAGE_VERSION),
    description="Cluster Pool Management",
    author='Damion K. Wilson',
    include_package_data=True,
    platforms='any',

    install_requires=[
        "paramiko",
    ],

    packages = [
        PACKAGE_NAME,
    ],

    package_data={
        '': ['examples/*'],
    },

    entry_points = {
        'console_scripts': [
            "poolman_console = {}.entry_points:console".format(PACKAGE_NAME),
        ]
    },
)
