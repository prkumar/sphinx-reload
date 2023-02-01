# Standard library imports
from setuptools import setup, find_packages
import os

# Local imports
with open(os.path.join(os.path.dirname(__file__), "sphinx_reload.py"), "r") as f:
    for line in f:
        if "__version__ = " in line:
            __version__ = eval(line.split("=")[1].strip())
            break


def read(filename):
    with open(filename) as stream:
        return stream.read()


metadata = dict({
    "name": "sphinx-reload",
    "author": "P. Raj Kumar",
    "author_email": "raj.pritvi.kumar@gmail.com",
    "version": __version__,
    "url": "https://github.com/prkumar/sphinx-reload",
    "license": "MIT",
    "description": "Live preview your Sphinx documentation",
    "long_description": read("README.rst"),
    "classifiers": [
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Documentation"
    ],
    "keywords": "sphinx live preview sync reload documentation",
    "install_requires": [
        "livereload >= 2.5.1",
    ],
    "py_modules": ["sphinx_reload"],
    "entry_points": {
        "console_scripts": [
            "sphinx-reload = sphinx_reload:main"
        ]
    }
})

if __name__ == "__main__":
    setup(**metadata)
