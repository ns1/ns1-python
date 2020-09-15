from setuptools import setup, find_packages

from codecs import open
from os import path
import ns1

cwd = path.abspath(path.dirname(__file__))

with open(path.join(cwd, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ns1-python",
    # flake8: noqa
    version=ns1.version,
    description="Python SDK for the NS1 DNS platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    # contact information
    author="NS1 Developers",
    author_email="devteam@ns1.com",
    url="https://github.com/ns1/ns1-python",
    packages=find_packages(exclude=["tests", "examples"]),
    setup_requires=[
        "pytest-runner",
        "wheel",
    ],
    tests_require=[
        "pytest",
        "pytest-pep8",
        "pytest-cov",
        "mock",
    ],
    keywords="dns development rest sdk ns1 nsone",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: Name Service (DNS)",
    ],
)
