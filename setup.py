#!/usr/bin/env python

import os
from setuptools import setup, find_packages

__version__ = "0.2.6"


def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as fp:
            return fp.read()
    except IOError:
        return ""


setup(
    name="cbadc-deltasigma",
    version=__version__,
    packages=find_packages(exclude=["beta", "cbadc_deltasigma.tests", "cbadc_deltasigma.tests.*"]),
    install_requires=["numpy", "scipy", "matplotlib>=3.0.0"],
    python_requires=">=3.11",
    zip_safe=False,
    include_package_data=False,
    license_files=["LICENSE"],
    author="Giuseppe Venturini and others",
    author_email="giuseppe.g.venturini@ieee.org",
    description="a Python package to synthesize, simulate, scale and map "
    + "to implementable topologies delta sigma modulators.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license="BSD-2-Clause",
    keywords="delta sigma modulator simulator",
    url="https://github.com/hammal/cbadc-deltasigma",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: 3.15",
    ],
)
