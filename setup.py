# Standard library imports
from setuptools import setup


def read(filename):
    with open(filename) as stream:
        return stream.read()


metadata = dict({
    "name": "sphinx-reload",
    "author": "P. Raj Kumar",
    "author_email": "raj.pritvi.kumar@gmail.com",
    "version": "0.1.0",
    "url": "https://github.com/prkumar/sphinx-reload",
    "license": "MIT",
    "description": "Live Reload Sphinx Documentation.",
    "long_description": read("README.rst"),
    "classifiers": [
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
    ],
    "keywords": "sphinx livereload documentation",
    "install_requires": [
        "livereload == 2.5.1",
    ],
})

if __name__ == "__main__":
    setup(**metadata)
