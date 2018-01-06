#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import os
import sys

from distutils.core import setup

pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))

# Get the current package version.
version_ns = {}
with open(pjoin(here, 'version.py')) as f:
    exec(f.read(), {}, version_ns)

setup_args = dict(
        name='nerscspawner',
        packages=['nerscspawner'],
        version=version_ns['__version__'],
        description="""NERSC Spawner: Custom spawners for Jupyterhub to spawn
        notebooks at NERSC in various ways""",
        long_description="""Spawn Jupyter notebooks on a remote node over SSH.
        In a running Docker container, login node, or batch job.""",
        author="Rollin Thomas, Shane Canon, Shreyas Cholia",
        author_email="rcthomas@lbl.gov, scanon@lbl.gov, scholia@lbl.gov",
        url="http://www.nersc.gov",
        license="BSD",
        platforms="Linux, Mac OS X",
        keywords=['Interactive', 'Interpreter', 'Shell', 'Web'],
        classifiers=[
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
        ],
)

# setuptools requirements
if 'setuptools' in sys.modules:
    setup_args['install_requires'] = install_requires = []
    with open('requirements.txt') as f:
        for line in f.readlines():
            req = line.strip()
            if not req or req.startswith(('-e', '#')):
                continue
            install_requires.append(req)


def main():
    setup(**setup_args)

if __name__ == '__main__':
    sys.exit(main())
