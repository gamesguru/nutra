# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 16:01:31 2020

@author: shane

This file is part of nutra, a nutrient analysis program.
    https://github.com/nutratech/cli
    https://pypi.org/project/nutra/

nutra is an extensible nutrient analysis and composition application.
Copyright (C) 2018-2020  Shane Jaroch

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

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
__dbtarget__ = "0.0.3"


# Onboarding function
def verify_db(force_install=False):
    cwd = os.path.expanduser("~/.nutra/db")

    # TODO: put this in main __init__? Require License agreement?
    if not os.path.exists(cwd):
        print("mkdir -p ~/.nutra/db")
        os.makedirs(cwd, mode=0o755)

    if "nutra.db" not in os.listdir(cwd) or force_install:
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

        # Download nutra.db.tar.xz
        print(
            "curl -L https://bitbucket.org/dasheenster/nutra-utils/downloads/nutra-0.0.2.db.tar.xz -o nutra.db.tar.xz"
        )
        urllib.request.urlretrieve(
            f"https://bitbucket.org/dasheenster/nutra-utils/downloads/nutra-{__dbtarget__}.db.tar.xz",
            f"{cwd}/nutra.db.tar.xz",
            reporthook,
        )
        print()

        # Extract the archive
        # NOTE: in sqlfuncs() we verify version == __dbtarget__, and if needed invoke this method with force_install=True
        with tarfile.open(f"{cwd}/nutra.db.tar.xz", mode="r:xz") as f:
            try:
                print("tar xvf nutra.db.tar.xz")
                f.extractall(cwd)
            except Exception as e:
                print(repr(e))
                print("ERROR: corrupt tarball, removing. Please try the download again")
                print("rm -rf ~/.nutra/db")
                shutil.rmtree(cwd)
                exit()
        print("==> done downloading nutra.db")
