import os
import sys
from setuptools import setup

PKG = "logmuse"
REQDIR = "requirements"


def read_reqs(reqs_name):
    deps = []
    depsfile = os.path.join(REQDIR, "requirements-{}.txt".format(reqs_name))
    with open(depsfile, 'r') as f:
        for l in f:
            if not l.strip():
                continue
            deps.append(l)
    return deps


# Additional keyword arguments for setup().
extra = {}

# 2to3
if sys.version_info >= (3, ):
    extra["use_2to3"] = True
extra["install_requires"] = []

with open(os.path.join(PKG, "_version.py"), 'r') as versionfile:
    version = versionfile.readline().split()[-1].strip("\"'\n")

# Handle the pypi README (long description) formatting.
try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
    msg = "\033[032mPandoc conversion succeeded.\033[0m"
except(IOError, ImportError, OSError):
    msg = "\033[0;31mWarning: pandoc conversion failed! Readme should not be uploaded to pypi.\033[0m"
    long_description = open('README.md').read()

setup(
    name=PKG,
    packages=[PKG],
    version=version,
    description="Logging setup",
    long_description=long_description,
    long_description_content_type='text/markdown', 
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
    license="BSD-2-Clause",
    scripts=None,
    include_package_data=True,
    test_suite="tests",
    tests_require=read_reqs("dev"),
    setup_requires=(["pytest-runner"] if {"test", "pytest", "ptr"} & set(sys.argv) else []),
    **extra
)


print(msg)
