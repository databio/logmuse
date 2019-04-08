import os
import sys
from setuptools import setup

PKG = "logmuse"

# Additional keyword arguments for setup().
extra = {}
DEPENDENCIES = []

# 2to3
if sys.version_info >= (3, ):
    extra["use_2to3"] = True
extra["install_requires"] = DEPENDENCIES

with open(os.path.join(PKG, "_version.py"), 'r') as versionfile:
    version = versionfile.readline().split()[-1].strip("\"'\n")

# Handle the pypi README (long description) formatting.
try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
    print("Pandoc conversion succeeded")
except(IOError, ImportError, OSError):
    print("Warning: pandoc conversion failed!")
    long_description = open('README.md').read()

setup(
    name=PKG,
    packages=[PKG],
    version=version,
    description="Logging setup",
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="logging, workflow, logger, logs",
    url="https://github.com/databio/{}/".format(PKG),
    author=u"Vince Reuter, Nathan Sheffield",
    license="BSD2",
    scripts=None,
    include_package_data=True,
    **extra
)

