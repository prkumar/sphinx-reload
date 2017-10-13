"""
Live reload your Sphinx documentation.

TODO:
    * Support more powerful file patterns (e.g., "**")
"""
# Standard library imports
import argparse
import os
import tempfile

# Third-party imports
import livereload


class SphinxReload(object):
    _MAKE_CMD_TEMPLATE = "make html BUILDDIR=%s"

    def __init__(self, makefile_path, build_dir=None):
        if os.path.isfile(makefile_path):
            makefile_path = os.path.dirname(makefile_path)
        self._docs_root = os.path.abspath(makefile_path)
        self._build_dir = build_dir
        self._spy_on = []

    @property
    def docs_root(self):
        return self._docs_root

    def watch(self, *glob_names):
        self._spy_on.extend(glob_names)

    @property
    def _build_directory(self):
        if self._build_dir is None:
            return tempfile.mkdtemp()
        else:
            return os.path.abspath(self._build_dir)

    def run(self, port=5500):
        server = livereload.Server()
        build_dir = self._build_directory
        make_cmd = self._MAKE_CMD_TEMPLATE % build_dir
        shell = livereload.shell(make_cmd, cwd=self._docs_root)
        shell()  # Do an initial build.
        for pattern in self._spy_on:
            server.watch(pattern, shell)
        server.serve(root=os.path.join(build_dir, "html"), port=port)


def _create_parser():
    parser = argparse.ArgumentParser(prog="sphinx-reload")
    parser.add_argument(
        "root",
        help="Your documentation's root directory (i.e., the place where "
             "`sphinx-build` put the Makefile)."
    )
    parser.add_argument(
        "--watch",
        metavar="PATTERN",
        nargs="+",
        help="File patterns to watch for changes, on which documentation "
             "should be rebuilt and served again."
    )
    parser.add_argument(
        "-p",
        "--port",
        default=5500,
        type=int,
        help="The port number from which to serve your documentation.")
    return parser


def _estimate_source_directory(dir_root):
    if os.path.isfile(os.path.join(dir_root, "source", "conf.py")):
        return os.path.join(dir_root, "source")
    elif os.path.isfile(os.path.join(dir_root, "conf.py")):
        return dir_root
    else:
        raise ValueError(
            "Failed to estimate documentation source directory from "
            "path '%s'" % dir_root
        )


def main():
    parser = _create_parser()
    namespace = parser.parse_args()
    reload = SphinxReload(namespace.root)

    if namespace.watch is None:
        try:
            watch = [_estimate_source_directory(reload.docs_root)]
        except ValueError as err:
            parser.error(str(err))
            raise
    else:
        watch = namespace.watch

    reload.watch(*watch)
    reload.run(port=namespace.port)


if __name__ == "__main__":
    main()
