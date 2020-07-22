import os


def git_sha():
    """ Gets the git revision, if it exists in cwd """
    cwd = os.getcwd()

    try:
        from .__sha__ import __sha__
    except Exception as e1:
        import subprocess
        from .settings import TESTING

        if not TESTING:
            print(repr(e1))
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        try:
            __sha__ = (
                subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
                .decode()
                .rstrip()
            )
        except Exception as e2:
            print(repr(e2))
            __sha__ = None

    os.chdir(cwd)
    return __sha__


# Export for package level
__sha__ = git_sha()
