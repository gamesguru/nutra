Nutritracker
============

Extensible command-line tool for nutrient analysis.

*Requires:*

- Python 3.6.5 or later
- Package manager (pip3)
- Internet connection


Install PyPi release (from pip)
-------------------------------
:code:`pip install nutri`

(**Note:** use :code:`pip3` on Linux/macOS)

**Update to latest**

:code:`pip install -U nutri`

**Subscribe to the preview/beta channel**

:code:`pip install nutri --pre`

**Unsubscribe (back to stable)**
::

    pip uninstall nutri
    pip install nutri

Using the source-code directly
------------------------------
::

    git clone git@github.com:gamesguru/nutri.git    
    cd nutri    
    ./nutri -h


Currently Supported Data
========================
**USDA Stock database**

- Standard reference database, 8790 foods


**Relative USDA Extensions**

- Flavonoid, Isoflavonoids, and Proanthocyanidins


**Branded Foods Database**

- Pairs with USDA stock, has 300k foods


Usage
=====

Requires internet connection to remote server.

Run the :code:`nutri` script to output usage.

Usage: :code:`nutri <command>`


**Commands**
::

    config                  change name, age, and vitamin targets

    search                  search database by food name

    analyze | anl           critique a date (range), meal, recipe, or food

    remote                  login, logout, register, and online functions

    --help | -h             show help for a given command

    config                  change name, age, and vitamin targets
