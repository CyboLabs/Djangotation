#!/usr/bin/env python

from setuptools import setup


setup(name='Djangotation',
      version='0.0.1a1',
      description='Django annotation extended framework',
      author='Anthony King',
      author_email='anthonydking@slimroms.net',
      test_suite='runtests',
      packages=['djangotation'],
      install_requires=[
            'Django==1.9.7'
      ])
