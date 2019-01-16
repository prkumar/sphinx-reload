"""
Live reload your Sphinx documentation.

TODO:
    * Support more powerful file patterns (e.g., "**")
"""
# Standard library imports
import argparse
import glob
import os
import sys

# Third-party imports
import livereload
import livereload.watcher

__version__ = "0.1.2"


class _RecursiveGlobWatcher(livereload.watcher.Watcher):
    def is_glob_changed(self, path, ignore=None):
        files = glob.glob(path, recursive=True)
        return any(self.is_file_changed(f, ignore) for f in files)


class _SphinxResourceFactory(object):
    _MAKE_CMD = "make html"
    _SPHINX_BUILD_CMD_TEMPLATE = "sphinx-build %s %s"
    _DEFAULT_BUILD_DIRECTORY = "_build"

    @staticmethod
    def get_documentation_root(makefile_path):
        if os.path.isfile(makefile_path):
            makefile_path = os.path.dirname(makefile_path)
        return makefile_path

    @staticmethod
    def estimate_source_directory(doc_root):
        if os.path.isfile(os.path.join(doc_root, "source", "conf.py")):
            return os.path.join(doc_root, "source")
        elif os.path.isfile(os.path.join(doc_root, "conf.py")):
            return doc_root
        else:
            raise ValueError(
                "Failed to estimate documentation source directory from "
                "path '%s'" % doc_root
            )

    def get_build_directory(self, doc_root):
        return os.path.join(doc_root, self._DEFAULT_BUILD_DIRECTORY)

    def get_make_command(self, build_directory):
        make_cmd = self._MAKE_CMD
        if build_directory is not None:
            make_cmd += " BUILDDIR=%s" % build_directory
        return make_cmd

    def get_sphinx_build_command(self, source_directory, build_directory):
        return self._SPHINX_BUILD_CMD_TEMPLATE % (
            source_directory, build_directory
        )

    @staticmethod
    def get_html_directory(build_directory):
        return os.path.join(build_directory, "html")


class SphinxReload(object):

    def __init__(self):
        self._spy_on = []
        self._sphinx = _SphinxResourceFactory()

    def watch(self, *glob_names):
        self._spy_on.extend(glob_names)

    def _run(self, build_func, root, port):
        watcher = _RecursiveGlobWatcher() if sys.version_info >= (3, 5) else None
        server = livereload.Server(watcher=watcher)
        for pattern in self._spy_on:
            server.watch(pattern, build_func)
        build_func()  # Do an initial build.
        server.serve(
            root=root,
            port=port,
            open_url_delay=2,
            restart_delay=0.3,
        )

    def run(self, doc_root, build_dir=None, port=5500, use_makefile=True):
        # Set up sphinx resources
        doc_root = self._sphinx.get_documentation_root(doc_root)
        doc_root = os.path.abspath(doc_root)
        if build_dir is None:
            build_dir = self._sphinx.get_build_directory(doc_root)
        html_dir = self._sphinx.get_html_directory(build_dir)

        if use_makefile:
            build_cmd = self._sphinx.get_make_command(build_dir)
        else:
            source_dir = self._sphinx.estimate_source_directory(doc_root)
            build_cmd = self._sphinx.get_sphinx_build_command(
                source_dir, build_dir
            )
        build_func = livereload.shell(build_cmd, cwd=doc_root)
        self._run(build_func, html_dir, port=port)


def _create_parser():
    parser = argparse.ArgumentParser(prog="sphinx-reload")
    parser.add_argument(
        '--version',
        action='version',
        version='v%s' % __version__
    )
    parser.add_argument(
        "documentation_root",
        help="Your documentation's root directory (i.e., the place where "
             "`sphinx-build` put the Makefile)."
    )
    parser.add_argument(
        "--build-dir",
        help="The desired build directory.",
        default=None
    )
    parser.add_argument(
        "--watch",
        metavar="PATTERN",
        default=[],
        nargs="+",
        help="File patterns to watch for changes, on which documentation "
             "should be rebuilt and served again."
    )
    parser.add_argument(
        "-p",
        "--port",
        default=5500,
        type=int,
        help="The port number from which to serve your documentation."
    )
    return parser


def main():
    parser = _create_parser()
    namespace = parser.parse_args()
    reload = SphinxReload()
    reload.watch(*namespace.watch)

    if namespace.watch:
        reload.watch(*namespace.watch)
    else:
        sphinx = _SphinxResourceFactory()
        src = sphinx.estimate_source_directory(namespace.documentation_root)
        reload.watch(os.path.abspath(src))

    reload.run(
        namespace.documentation_root,
        build_dir=namespace.build_dir,
        port=namespace.port,
    )


if __name__ == "__main__":
    main()
