**************
 nutratracker
**************

.. image:: https://api.travis-ci.com/nutratech/cli.svg?branch=master
    :target: https://travis-ci.com/nutratech/cli
.. image:: https://pepy.tech/badge/nutra/month
    :target: https://pepy.tech/project/nutra/month
.. image:: https://img.shields.io/pypi/pyversions/nutra.svg
    :target: https://pypi.org/project/nutra

Extensible command-line tools for nutrient analysis.

*Requires:*

- Python 3.6.5 or later
- Package manager (pip3)
- Internet connection


See database: https://github.com/gamesguru/ntdb

See server:   https://github.com/gamesguru/nutra-server

Notes
=====

On macOS and Linux, you may need to add the following line to
your `.profile` file:

.. code-block:: bash

    export $PATH=$PATH:/usr/local/bin

On Windows you should check the box during the Python installer
to include `Scripts` directory in your `PATH`.  This can be done
manually after installation too.

Install PyPi release (from pip)
===============================
:code:`pip install nutra`

(**Note:** use :code:`pip3` on Linux/macOS)

**Update to latest**

:code:`pip install -U nutra`

Using the source-code directly
##############################
.. code-block:: bash

    git clone git@github.com:nutratech/cli.git
    cd nutra    
    pip3 install -r requirements.txt
    ./nutra -h

When building the PyPi release use the commands:

.. code-block:: bash

    python3 setup.py sdist
    twine upload dist/nutra-X.X.X.tar.gz

Currently Supported Data
========================

**USDA Stock database**

- Standard reference database (SR28)  [7794 foods]


**Relative USDA Extensions**

- Flavonoid, Isoflavonoids, and Proanthocyanidins  [1352 foods]

Usage
=====

Requires internet connection to remote server, or a locally running server (set env: `NUTRA_OVERRIDE_LOCAL_SERVER_HOST`).

Run the :code:`nutra` script to output usage.

Usage: :code:`nutra <command>`


Commands
########

::

    optional arguments:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit

    nutra subcommands:
    valid subcommands

    {search,sort,anl,day,nt}
                            additional help
        search              use to search foods and recipes
        sort                use to sort foods by nutrient ID
        anl                 use to analyze foods, recipes, logs
        day                 use to sort foods by nutrient ID
        nt                  list out nutrients and their info
