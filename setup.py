#!/usr/bin/env python
# encoding: utf-8
"""package program for UFT
"""
__version__ = "0.1"
__author__ = "@boqiling"

from setuptools import setup, find_packages

setup(
    name="UFT",
    version=__version__,
    #package_dir={'': 'src'},
    #packages=["UFT", "usb"],
    packages=find_packages(),
    package_data={'': ['*.xml', '*.dll', '*.so']},
    author=__author__,
    description='Agigatech Universal Function Test Program',
    platforms="any",
    entry_points={
        "console_scripts": [
            'uft = uft.main:main'
        ]
    }
)
