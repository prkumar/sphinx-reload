"""
Live reload your Sphinx documentation.

TODO:
    * Support more powerful file patterns (e.g., "**")
"""
# Standard library imports
import argparse
import glob
import os
import tempfile

# Third-party imports
import livereload
import livereload.watcher


class _RecursiveGlobWatcher(livereload.watcher.Watcher):
    def is_glob_changed(self, path, ignore=None):
        files = glob.glob(path, recursive=True)
        return any(self.is_file_changed(f, ignore) for f in files)


class _SphinxResourceFactory(object):
    _MAKE_CMD_TEMPLATE = "make html BUILDDIR=%s"

    @staticmethod
    def get_documentation_root(makefile_path):
        if os.path.isfile(makefile_path):
            return os.path.dirname(makefile_path)
        else:
            return makefile_path

    @staticmethod
    def get_source_directory(doc_root):
        if os.path.isfile(os.path.join(doc_root, "source", "conf.py")):
            return os.path.join(doc_root, "source")
        elif os.path.isfile(os.path.join(doc_root, "conf.py")):
            return doc_root
        else:
            raise ValueError(
                "Failed to estimate documentation source directory from "
                "path '%s'" % doc_root
            )

    def get_make_command(self, build_directory):
        return self._MAKE_CMD_TEMPLATE % build_directory

    @staticmethod
    def get_html_directory(build_dir):
        return os.path.join(build_dir, "html")


class SphinxReload(object):
    def __init__(self):
        self._spy_on = []

    @staticmethod
    def _get_build_directory(build_dir):
        if build_dir is None:
            return tempfile.mkdtemp()
        else:
            return os.path.abspath(build_dir)

    def watch(self, *glob_names):
        self._spy_on.extend(glob_names)

    def run(self, doc_root, build_dir=None, port=5500, watch_source=False):
        # Set up sphinx resources
        sphinx = _SphinxResourceFactory()
        doc_root = sphinx.get_documentation_root(doc_root)
        build_dir = self._get_build_directory(build_dir)
        make_cmd = sphinx.get_make_command(build_dir)
        html_dir = sphinx.get_html_directory(build_dir)

        spy_on = self._spy_on
        if watch_source:
            # Spy on changes in source directory.
            spy_on += [sphinx.get_source_directory(doc_root)]

        # Set up live preview server
        server = livereload.Server(watcher=_RecursiveGlobWatcher())
        shell = livereload.shell(make_cmd, cwd=doc_root)
        shell()  # Do an initial build.
        for pattern in spy_on:
            server.watch(pattern, shell)
        server.serve(root=html_dir, port=port)


def _create_parser():
    parser = argparse.ArgumentParser(prog="sphinx-reload")
    parser.add_argument(
        "documentation_root",
        help="Your documentation's root directory (i.e., the place where "
             "`sphinx-build` put the Makefile)."
    )
    parser.add_argument(
        "-b",
        "--build-dir",
        help="Your documentation's root directory (i.e., the place where "
             "`sphinx-build` put the Makefile)."
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
    reload.run(
        namespace.documentation_root,
        namespace.build_dir,
        port=namespace.port,
        watch_source=bool(namespace.watch)
    )


if __name__ == "__main__":
    main()
