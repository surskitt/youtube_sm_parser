#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.readlines()

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Shane Donohoe",
    author_email='shane@donohoe.cc',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Output youtube subscriptions using subscription_manager file",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            'youtube_sm_parser = youtube_sm_parser.youtube_sm_parser:main'
        ]
    },
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='youtube_sm_parser',
    name='youtube_sm_parser',
    packages=find_packages(include=['youtube_sm_parser']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/shanedabes/youtube_sm_parser',
    version='0.1.4',
    zip_safe=False,
)
