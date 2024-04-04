import os
import sys
from setuptools import setup

PKG = "logmuse"
REQDIR = "requirements"


def read_reqs(reqs_name):
    deps = []
    depsfile = os.path.join(REQDIR, "requirements-{}.txt".format(reqs_name))
    with open(depsfile, "r") as f:
        for l in f:
            if not l.strip():
                continue
            deps.append(l)
    return deps


# Additional keyword arguments for setup().
extra = {}

DEPENDENCIES = []
with open("requirements/requirements-all.txt", "r") as reqs_file:
    for line in reqs_file:
        if not line.strip():
            continue
        DEPENDENCIES.append(line)

extra["install_requires"] = DEPENDENCIES


with open(os.path.join(PKG, "_version.py"), "r") as versionfile:
    version = versionfile.readline().split()[-1].strip("\"'\n")

# Handle the pypi README formatting.
with open("README.md") as f:
    long_description = f.read()

setup(
    name=PKG,
    packages=[PKG],
    version=version,
    description="Logging setup",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="logging, workflow, logger, logs",
    url="https://github.com/databio/{}/".format(PKG),
    author="Vince Reuter, Nathan Sheffield",
    license="BSD-2-Clause",
    scripts=None,
    include_package_data=True,
    test_suite="tests",
    tests_require=read_reqs("dev"),
    setup_requires=(
        ["pytest-runner"] if {"test", "pytest", "ptr"} & set(sys.argv) else []
    ),
    **extra
)
