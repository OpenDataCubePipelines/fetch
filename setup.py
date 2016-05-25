#!/usr/bin/env python2.7
from __future__ import print_function

import os

from setuptools import setup

version = '1.1.4b'

# Append TeamCity build number if it gives us one.
if 'TC_BUILD_NUMBER' in os.environ and version.endswith('b'):
    version += '' + os.environ['TC_BUILD_NUMBER']

setup(name='fetch',
      maintainer='Jeremy Hooke',
      maintainer_email='jeremy.hooke@ga.gov.au',
      version=version,
      description='Automatic retrieval of ancillary and data',
      packages=[
          'fetch',
          'fetch.scripts'
      ],
      install_requires=[
          'arrow',
          'croniter',
          'feedparser',
          'lxml',
          'pathlib',
          'pyyaml',
          'requests',
          'setproctitle',
      ],
      entry_points={
          'console_scripts': [
              'fetch-service = fetch.scripts.service:main'
              'fetch-once = fetch.scripts.once:main'
          ]
      },
      )
