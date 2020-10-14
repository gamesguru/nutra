import os
import sys

from dotenv import load_dotenv

from .utils.gitutils import git_sha

# Check Python version
PY_MIN_VER = (3, 6, 5)
PY_MIN_STR = ".".join(str(x) for x in PY_MIN_VER)
if sys.version_info < PY_MIN_VER:
    ver = ".".join([str(x) for x in sys.version_info[0:3]])
    print("ERROR: nutra requires Python %s or later to run" % PY_MIN_STR)
    print("HINT:  You're running Python " + ver)
    exit(1)

# Read in .env file if it exists locally, else look to env vars
load_dotenv(verbose=False)

NUTRA_DIR = os.path.join(os.path.expanduser("~"), ".nutra")

# Set DB versions here
__db_target_usda__ = "0.0.7"
__db_target_nt__ = "0.0.0"


# Package info
__title__ = "nutra"
__version__ = "0.2.0.dev0"
__sha__ = git_sha()
__author__ = "Shane Jaroch"
__license__ = "GPL v3"
__copyright__ = "Copyright 2018-2020 Shane Jaroch"
