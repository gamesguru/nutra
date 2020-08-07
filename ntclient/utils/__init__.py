import os
import shutil
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
__dbtarget__ = "0.0.2"
__dbsha__ = "36fb0ba513d75271e1540e03a5115b25b2b1c08464f4f7e9147cb5dc87e9b4e5"


# Onboarding function
def verify_db(force_install=False):
    cwd = os.path.expanduser("~/.nutra/db")

    # TODO: put this in main __init__? Require License agreement?
    if not os.path.exists(cwd):
        os.makedirs(cwd, mode=0o755)

    # TODO: require db_ver() >= __dbtarget__
    if "nutra.db" not in os.listdir(cwd) or force_install:
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

        # Download nutra.db.tar.xz
        urllib.request.urlretrieve(
            f"https://bitbucket.org/dasheenster/nutra-utils/downloads/nutra-{__dbtarget__}.db.tar.xz",
            f"{cwd}/nutra.db.tar.xz",
            reporthook,
        )

        # TODO: verify db version
        with tarfile.open(f"{cwd}/nutra.db.tar.xz", mode="r:xz") as f:
            try:
                f.extractall(cwd)
            except Exception as e:
                print(repr(e))
                print("ERROR: corrupt tarball, removing. Please try the download again")
                shutil.rmtree(cwd)
                exit()
        print("==> done downloading nutra.db")
