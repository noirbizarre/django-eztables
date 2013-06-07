#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from os.path import join
from setuptools import setup, find_packages

RE_REQUIREMENT = re.compile(r'^\s*-r\s*(?P<filename>.*)$')

PYPI_RST_FILTERS = (
    # Replace code-blocks
    (r'\.\.\s? code-block::\s*(\w|\+)+',  '::'),
    # Remove travis ci badge
    (r'.*travis-ci\.org/.*', ''),
)


def rst(filename):
    '''
    Load rst file and sanitize it for PyPI.
    Remove unsupported github tags:
     - code-block directive
     - travis ci build badge
    '''
    content = open(filename).read()
    for regex, replacement in PYPI_RST_FILTERS:
        content = re.sub(regex, replacement, content)
    return content


def pip(filename):
    '''Parse pip requirement file and transform it to setuptools requirements'''
    requirements = []
    for line in open(join('requirements', filename)).readlines():
        match = RE_REQUIREMENT.match(line)
        if match:
            requirements.extend(pip(match.group('filename')))
        else:
            requirements.append(line)
    return requirements


long_description = '\n'.join((
    rst('README.rst'),
    rst('CHANGELOG.rst'),
    ''
))

setup(
    name='django-eztables',
    version=__import__('eztables').__version__,
    description=__import__('eztables').__description__,
    long_description=long_description,
    url='https://github.com/noirbizarre/django-eztables',
    download_url='http://pypi.python.org/pypi/django-eztables',
    author='Axel Haustant',
    author_email='noirbizarre+django@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=pip('install.pip'),
    tests_require=pip('test.pip'),
    license='LGPL',
    use_2to3=True,
    classifiers=[
        "Framework :: Django",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3',
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: System :: Software Distribution",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3',
        "Topic :: Software Development :: Libraries :: Python Modules",
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    ],
)
