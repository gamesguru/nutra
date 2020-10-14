import os


def git_sha():
    """ Gets the git revision, if it exists in cwd """
    cwd = os.getcwd()

    try:
        from .. import __sha__
    except ImportError as e1:
        import subprocess

        # TODO: import VERBOSITY from utils, print on >1 ?
        # print(repr(e1))
        cwd = os.path.dirname(os.path.abspath(__file__))

        try:
            __sha__ = (
                subprocess.check_output(
                    ["git", "rev-parse", "--short", "HEAD"], cwd=cwd
                )
                .decode()
                .rstrip()
            )
        except FileNotFoundError as e2:
            # print(repr(e2))
            __sha__ = None

    return __sha__
