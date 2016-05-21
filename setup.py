#!/usr/bin/python

from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='foscam',
    version='1.0',
    description='Hashicorp vault backend for python-keyring',
    long_description=read('README.md'),
    author='Philipp Schmitt',
    author_email='philipp.schmitt@post.lu',
    url='https://github.com/quatanium/foscam-python-lib',
    packages=find_packages(),
)
