#!/usr/bin/env python
"""
Find AWS EC2 AMIs for Canonical Ubuntu images
"""

from setuptools import setup

from canonical_amis import get_version

doc = __doc__.strip("\n")

classifiers = """
Development Status :: 4 - Beta
Intended Audience :: System Administrators
License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: OS Independent
"""

name = "canonical-amis"
module = 'canonical_amis'
version = get_version()

def github_url(owner, name):
	return 'https://github.com/{}/{}'.format(owner, name)

def download_url(name, version):
    fmt = 'https://pypi.python.org/packages/source/{0}/{1}/{1}-{2}.tar.gz'
    return fmt.format(name[0], name, version)

setup(name=            name,
      version=         version,
      url=             github_url('divitu', name),
      download_url=    download_url(name, version),
      author=          "Colin von Heuring",
      author_email=    "colin@von.heuri.ng",
      description=     doc,
      classifiers=     filter(None, classifiers.split("\n")),
      license=         "GNU General Public License",
      platforms=       ['any'],
      install_requires=['boto'],
      py_modules=      [module],
      scripts=         [name])
