# Standard library imports
from setuptools import setup, find_packages


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
    "description": "Sphinx Documentation Live.",
    "long_description": read("README.rst"),
    "classifiers": [
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        # TODO: Verify that script works on other Python versions.
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Documentation"
    ],
    "keywords": "sphinx live preview sync reload documentation",
    "install_requires": [
        "livereload >= 2.5.1",
    ],
    "packages": find_packages(),
    "entry_points": {
        "console_scripts": [
            "sphinx-reload = sphinx_reload:main"
        ]
    }
})

if __name__ == "__main__":
    setup(**metadata)
