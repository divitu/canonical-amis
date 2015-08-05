#!/usr/bin/env python

from distutils.core import setup

setup(name='canonical_amis',
      version='0.1',
      description='Find AWS EC2 AMIs for Canonical Ubuntu images',
      install_requires=['boto'],
      modules=['canonical_amis'],
      scripts=['canonical-amis'])
