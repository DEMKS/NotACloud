#!/usr/bin/env python
import io
import re
from setuptools import setup, find_packages
import sys

with io.open('./TestApp/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='TestApp',
    version=version,
    description='This is not a App',
    long_description=long_description,
    author='NotADevs',
    author_email='NAD@gmail.com',
    license='GNU General Public License v3 or later (GPLv3+)',
    packages=find_packages(
        exclude=[
            'docs', 'tests',
            'windows', 'macOS', 'linux',
            'iOS', 'android',
            'django'
        ]
    ),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
    install_requires=[
        'pyside2==5.13.0',
    ],
    options={
        'app': {
            'formal_name': 'Test',
            'bundle': 'com.NAD'
        },

        # Desktop/laptop deployments
        'macos': {
            'app_requires': [
            ]
        },
        'linux': {
            'app_requires': [
            ]
        },
        'windows': {
            'app_requires': [
            ]
        },

        # Mobile deployments
        'ios': {
            'app_requires': [
            ]
        },
        'android': {
            'app_requires': [
            ]
        },

        # Web deployments
        'django': {
            'app_requires': [
            ]
        },
    }
)
