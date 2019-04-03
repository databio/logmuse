import os
import sys
from setuptools import setup


PKG = "logmuse"
REQDIR = "requirements"


def read_reqs(reqs_name):
    deps = []
    fp = os.path.join(REQDIR, "requirements-{}.txt".format(reqs_name))
    with open(fp, 'r') as f:
        for l in f:
            if not l.strip():
                continue
            deps.append(l)
    return deps


# Additional keyword arguments for setup().
extra = {}

# Ordinary dependencies
DEPENDENCIES = read_reqs("all")

# 2to3
if sys.version_info >= (3, ):
    extra["use_2to3"] = True
extra["install_requires"] = DEPENDENCIES


with open("{}/_version.py".format(PKG), 'r') as versionfile:
    version = versionfile.readline().split()[-1].strip("\"'\n")

# Handle the pypi README formatting.
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
    url="https://github.com/vreuter/{}/".format(PKG),
    author=u"Vince Reuter",
    license="BSD2",
    scripts=None,
    include_package_data=True,
    test_suite="tests",
    tests_require=read_reqs("dev"),
    setup_requires=(["pytest-runner"] if {"test", "pytest", "ptr"} & set(sys.argv) else []),
    **extra
)
