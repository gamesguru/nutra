Nutritracker
------------

An extensible nutrient tracking app designed for home and office use.
CLI backend.

*Requires:*

- Python 3.6.5 or later
- Desktop (Win/mac/Linux)
- *(Optional)* Android 5.0+ phone, USB, adb, developer mode

Downloading Food Data
=====================
Can be downloaded manually, visit these links:

https://bitbucket.org/dasheenster/nutri-utils/downloads/

https://ndb.nal.usda.gov/ndb/search (see downloads, ASCII not Access)

These can also be downloaded from the Android app, or synced over USB cable, with the exception of the Branded foods database.  This can also be loaded onto phones by force, but it will slow the app down at start-time since it contains over 300 thousand foods with full ingredient lists.

Available resources
^^^^^^^^^^^^^^^^^^^
Installing from Release
"""""""""""""""""""""""
The PyPi release, which can be installed on Python >3.6.5 with :code:`pip install nutri`, ships by default with:

1) The USDAstock database,
2) Supplementary flavonoid database, and
3) Extra fields (IF, ORAC, GI).

No configuration is required in the release, but when adding your own or doing the process from scratch you will need to pair column names with known nutrient names in a "config.txt".

The full database import process is explained with :code:`nutri db --help`

Downloading Resources
"""""""""""""""""""""

You can download resources from mac/Linux terminal.

`Curl for Windows <https://curl.haxx.se/windows/>`_ requires it be put in the $PATH variable.  Better directions for getting set up on Windows will be (eventually) posted `on youtube <https://www.youtube.com/user/gamesguru>`_.

So Windows users can simply download with a web browser:

https://bitbucket.org/dasheenster/nutri-utils/downloads/

**Databases**

- Standard USDA database, 8790 foods

    `curl -L https://api.bitbucket.org/2.0/repositories/dasheenster/nutri-utils/downloads/USDAstock.txt -o USDAstock.txt`

- Branded Foods Database. **LARGE 100MB+! PC ONLY**

    `curl -L https://www.ars.usda.gov/ARSUserFiles/80400525/Data/BFPDB/BFPD_csv_07132018.zip -o BFPD_csv_07132018.zip`

**Supplementary USDA Extensions**

- Flavonoid, Isoflavonoids, and Proanthocyanidins

    `curl -L https://api.bitbucket.org/2.0/repositories/dasheenster/nutri-utils/downloads/USDA_ext_rel.zip -o USDA_ext_rel.zip`

**Extra Fields**

**Note:** We are trying to start a collection of fields and make our models more general. Please upload and get in touch at `gitter.im/nutritracker/nutri <https://gitter.im/nutritracker/nutri>`_  ... (these can consist in magazine cutouts, obscure articles, or other sources of nutrient data)

- `IF <https://inflammationfactor.com/if-rating-system/>`_, `ORAC <https://www.superfoodly.com/orac-values/>`_, GI, Omega-3, and (anti-nutrient?) oxalic acid

    `curl -L  https://api.bitbucket.org/2.0/repositories/dasheenster/nutri-utils/downloads/Extra_fields.zip -o Extra_fields.zip`


Getting Set Up
==============
You need to make a user first, then import DBs with  :code:`nutri db --help`.  After that you can pair fields and add custom foods.  Or just use the stock database to start making recipes and tracking simple meals.

Eventually you can track more fields and metrics on a daily basis, include more on your log, get to know your habits, and benefit from automated suggestions.

Due to the localized nature of the program (i.e. it runs for your computer, on your computer) we are able to outperform some websites in searches.  We can update your search results AS YOU TYPE.  But for the same reason we also face limitations, such as not having a very large Barcode database, or community-driven input.  Mostly we add data to the stock set when someone submits an interesting sample, perhaps only 30 foods.

Generating Log Reports
^^^^^^^^^^^^^^^^^^^^^^
With the :code:`log` function, you can get detailed information printed in porcelain, color, or chart form (percentages, macros, extendeds, lowest/highest score).  It's possible to filter by date range or nutrient type.  Eventually we will make a seperate analysis command, to analyse any ingredient, food, or recipe across the standard metrics.

The Android app may be more intuitive for people less familiar with computers, it offers many of the same features and we are constantly working to improve that.

Eventually someone can make a GUI interface for the computer that parses the porcelain output, and that may be easier to use.

Usage
^^^^^

Run the :code:`nutri` script to output usage.

Usage: :code:`nutri <command>`

**Commands**
::

    config                  change name, age, and vitamin targets

    db                      import, edit and verify databases

    field                   import, pair and manage fields

    recipe                  create, edit and view foods and recipes

    search                  search databases or recipes

    add                     add foods or items to daily log

    log                     show previous meals and summary

    sync                    sync android device

    contrib                 rank contribution

    bugreport               e-wires source code and your pesonal info

    --help | -h             show help for a given command
