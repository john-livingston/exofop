#!/usr/bin/env python
import os
import sys
import re

try:
    from setuptools import setup
    setup
except ImportError:
    from distutils.core import setup
    setup

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

# Handle encoding
major, minor1, minor2, release, serial = sys.version_info
if major >= 3:
    def rd(filename):
        f = open(filename, encoding="utf-8")
        r = f.read()
        f.close()
        return r
else:
    def rd(filename):
        f = open(filename)
        r = f.read()
        f.close()
        return r

setup(
    name='exofop',
    packages =['exofop'],
    version="0.1.1",
    author='John Livingston and Jerome de Leon',
    author_email = 'jpdeleon@astron.s.u-tokyo.ac.jp',
    url = 'https://github.com/jpdeleon/exofop',
    license = ['GNU GPLv3'],
    description ='Scraper for the ExoFOP K2 community portal website',
    long_description=rd("README.md") + "\n\n"
                    + "---------\n\n",
    package_dir={"exofop": "exofop"},
    package_data={"exofop": []},
    scripts=['scripts/get_star_ini','scripts/get_links'],
    include_package_data=True,
    keywords=[],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python'
        ],
    install_requires = ['BeautifulSoup4','urllib3'],
)
