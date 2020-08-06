import os
import sys
import tarfile
import time
import urllib.request


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
        cwd = os.path.dirname(os.path.abspath(__file__))

        try:
            __sha__ = (
                subprocess.check_output(
                    ["git", "rev-parse", "--short", "HEAD"], cwd=cwd
                )
                .decode()
                .rstrip()
            )
        except Exception as e2:
            print(repr(e2))
            __sha__ = None

    return __sha__


# Export for package level
__sha__ = git_sha()
__dbver__ = "0.0.0"
__dbsha__ = "3cd2087cdb7a104e62d708c58eb6036fdcf1365562d3b03d483656625b568560"


# Onboarding function
def verify_db():
    cwd = os.path.expanduser("~/.nutra")
    if "nutra.db" not in os.listdir(cwd):
        """Downloads and unpacks the nt-sqlite3 db"""

        def reporthook(count, block_size, total_size):
            """ Shows download progress """
            global start_time
            if count == 0:
                start_time = time.time()
                time.sleep(0.01)
                return
            duration = time.time() - start_time
            progress_size = int(count * block_size)
            speed = int(progress_size / (1024 * duration))
            percent = int(count * block_size * 100 / total_size)
            sys.stdout.write(
                "\r...%d%%, %d MB, %d KB/s, %d seconds passed"
                % (percent, progress_size / (1024 * 1024), speed, duration)
            )
            sys.stdout.flush()

        if "nutra.db.tar.xz" not in os.listdir(cwd):
            # Download nutra.db.tar.xz
            urllib.request.urlretrieve(
                f"https://bitbucket.org/dasheenster/nutra-utils/downloads/nutra-{__dbver__}.db.tar.xz",
                f"{cwd}/nutra.db.tar.xz",
                reporthook,
            )
        # Extract
        with tarfile.open(f"{cwd}/nutra.db.tar.xz", mode="r:xz") as f:
            f.extractall(cwd)
        print("==> done downloading nutra.db")
