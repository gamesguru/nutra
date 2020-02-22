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

**Subscribe to the preview/beta channel**

:code:`pip install nutra --pre`

**Unsubscribe (back to stable)**

.. code-block:: bash

    pip uninstall nutra
    pip install nutra

Using the source-code directly
##############################
.. code-block:: bash

    git clone git@github.com:gamesguru/nutra.git
    pip3 install -r requirements.txt
    cd nutra    
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

Advanced Features
=================

Features such as adding to a food log and creating recipes require logging in.

First use the :code:`register` command to create an account, then :code:`login`.

Usage
=====

Requires internet connection to remote server.

Run the :code:`nutra` script to output usage.

Usage: :code:`nutra <command>`


Commands
########

::

    config                  change name, age, and vitamin targets

    search                  search database by food name

    analyze | anl           critique a date (range), meal, recipe, or food

    --help | -h             show help for a given command
