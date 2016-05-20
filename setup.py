from __future__ import with_statement
from setuptools import setup
import sys


with open("README.rst") as f:
    readme = f.read()


setup(
    name="skiski",
    version="0.1.0",
    description="SKI Combinator for Python",
    long_description=readme,
    author="esehara shigeo",
    author_email="esehara@gmail.com",
    url="https://github.com/esehara/skiski",
    py_modules=["skiski"],
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ]
)
