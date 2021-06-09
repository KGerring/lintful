#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0',
                'pip==19.2',
                'bumpversion==0.5.3',
                'wheel==0.30.0',
                'watchdog==0.8.3',
                'flake8==3.5.0',
                'tox==2.9.1',
                'coverage==4.5.1',
                'Sphinx==1.7.2',
                'addict',
                'astroid',
                'logilab',
                'pylint',
                'regex',
                'six',
                'yaml']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Kristen Gerring",
    author_email='KGerring@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
     
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="""Helpers/Serializers/reporters etc for pylint""",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='lintful pylint static code flake lint',
    name='lintful',
    packages=find_packages(include=['lintful']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/kgerring/lintful',
    version='0.1.2',
    zip_safe=False,
)
