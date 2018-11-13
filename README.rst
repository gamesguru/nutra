Nutritracker
============

Extensible command-line tool for nutrient analysis.

*Requires:*

- Python 3.6.5 or later
- Desktop: Windows, macOS, or Linux
- *(Optional)* Android 5.0+ phone, USB, adb, developer mode


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


Downloading Food Data
=====================

Linux/macOS Script (curl)
-------------------------
::

    cd ~
    curl -L https://api.bitbucket.org/2.0/repositories/dasheenster/nutri-utils/downloads/nutri.zip -o nutri.zip
    unzip -o nutri.zip
    rm nutri.zip

Windows (web download)
----------------------
Download :code:`nutri.zip`:

https://bitbucket.org/dasheenster/nutri-utils/downloads/

Extract the :code:`.nutri` folder to your home folder.


- On Windows this is :code:`C:\Users\<your_name>`
- On macOS it's :code:`/Users/<your_name>`
- On Linux it's :code:`/home/<your_name>`

These can also be downloaded from the Android app, or synced over USB cable.

You can also import your own flat file databases.  The full database import process is explained with :code:`nutri db --help`

Better directions for getting set up (on Windows) will (eventually) be posted `on youtube <https://www.youtube.com/user/gamesguru>`_.


Currently Supported Data
========================
**USDA Stock database**

- Standard flat file database, 8790 foods


**Relative USDA Extensions**

- Flavonoid, Isoflavonoids, and Proanthocyanidins


**Extra Fields**

- `IF <https://inflammationfactor.com/if-rating-system/>`_, `ORAC <https://www.superfoodly.com/orac-values/>`_, GI, Omega-3, and (anti-nutrients) oxalic acid, mercury, etc


**Note:** We are trying to start a collection of fields and make our models more general. Please upload and get in touch at `gitter.im/nutritracker/nutri <https://gitter.im/nutritracker/nutri>`_  ... (these can consist in magazine cutouts, NCBI tables, or other sources of nutrient data)


Not Supported Yet
=================

**Branded Foods Database**

- (LARGE 100MB+! PC ONLY)

**Canadian Nutrient Files**

- Similar to USDAstock, except relational (not flat file)


Usage
=====

Many features will require you to do the editing in notepad or your favorite text editor.  Then you can use the :code:`analyze` command to perform the analyses.

Run the :code:`nutri` script to output usage.

Usage: :code:`nutri <command>`


**Commands**
::

    config                  change name, age, and vitamin targets

    db                      import, edit and verify databases

    field                   import, pair and manage fields

    search                  search databases or recipes

    analyze | anl           critique a date (range), meal, recipe, or food

    sync                    sync android device

    bugreport               upload database info, and version number

    --help | -h             show help for a given command
