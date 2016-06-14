import os
import sys
import nsone

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

tests_require = [
    'pytest',
    'pytest-pep8',
    'pytest-cov',
    'mock',
]

setup(
    name='nsone',
    # flake8: noqa
    version=nsone.version,
    description='Python SDK for the NSONE DNS platform',
    author='Shannon Weyrick',
    author_email='sweyrick@nsone.net',
    url='https://github.com/nsone/nsone-python',
    packages=['nsone', 'nsone.rest', 'nsone.rest.transport'],
    setup_requires=['pytest-runner'],
    tests_require=tests_require,
    keywords='dns development rest sdk nsone',
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
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: Name Service (DNS)"
    ])
