import os
import shutil
import sqlite3
import sys
import tarfile
import time
import urllib.request

from .... import __db_target_usda__
from ... import NUTRA_DIR


# Onboarding function
def verify_usda(__db_target_usda__, force_install=False):
    CWD = f"{NUTRA_DIR}/usda"

    # TODO: put this in main __init__? Require License agreement?
    if not os.path.exists(CWD):
        print("mkdir -p ~/.nutra/usda")
        os.makedirs(CWD, mode=0o755)

    if "usda.sqlite" not in os.listdir(CWD) or force_install:
        """Downloads and unpacks the nt-sqlite3 db"""

        def reporthook(count, block_size, total_size):
            """Shows download progress"""
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

        # Download usda.sqlite.tar.xz
        url = f"https://bitbucket.org/dasheenster/nutra-utils/downloads/usda.sqlite-{__db_target_usda__}.tar.xz"
        print(f"curl -L {url} -o usda.sqlite.tar.xz")
        urllib.request.urlretrieve(
            url, f"{CWD}/usda.sqlite.tar.xz", reporthook,
        )
        print()

        # Extract the archive
        # NOTE: in sql.__init__() we verify version == __db_target_usda__, and if needed invoke this method with force_install=True
        with tarfile.open(f"{CWD}/usda.sqlite.tar.xz", mode="r:xz") as f:
            try:
                print("tar xvf usda.sqlite.tar.xz")
                f.extractall(CWD)
            except Exception as e:
                print(repr(e))
                print("ERROR: corrupt tarball, removing. Please try the download again")
                print("rm -rf ~/.nutra/usda")
                shutil.rmtree(CWD)
                exit()
        print("==> done downloading usda.sqlite")


# verify_usda(__db_target_usda__)

# Connect to DB
# TODO: support as customizable env var ?
db_path = os.path.expanduser(f"{NUTRA_DIR}/usda/usda.sqlite")
if os.path.isfile(db_path):
    con = sqlite3.connect(db_path)
    # con.row_factory = sqlite3.Row  # see: https://chrisostrouchov.com/post/python_sqlite/
else:
    # print("warn: usda database doesn't exist, please run init")
    # print("info: init not implemented, manually copy")
    con = None


def _sql(query, headers=False):
    """Executes a SQL command to usda.sqlite"""
    # TODO: DEBUG flag or VERBOSITY level in prefs.json ... Print off all queries

    cur = con.cursor()
    result = cur.execute(query)
    rows = result.fetchall()
    if headers:
        headers = [x[0] for x in result.description]
        return headers, rows
    return rows
