from __future__ import print_function, unicode_literals
from setuptools import setup, find_packages

from distutils.core import setup

__author__ = "fowbi"

with open("README.rst", 'r') as file:
    readme = file.read()

with open("LICENSE", 'r') as file:
    license = file.read()

setup(
    name='lint-along',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/fowbi/lint-along',
    license=license,
    zip_safe=False,
    keywords='lint-along ',
    author='fowbi',
    author_email='dev@magier.com',
    description='lint-along',
    long_description=readme,
    entry_points={
        "console_scripts": [
            'lint-along = lintalong.cli:cli'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
