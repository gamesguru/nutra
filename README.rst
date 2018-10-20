Nutritracker
------------

An extensible nutrient tracking app designed for home and office use.
CLI backend.

*Requires:*

- Python 3.6.5 or later
- Desktop (Win/mac/Linux)
- *(Optional)* Android 5.0+ phone, USB, developer mode

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
The PyPi release, which can be installed on Python >3.6.5 with `pip install nutri`, ships by default with:

1) The USDAstock database,
2) Supplementary flavonoid database, and
3) Extra fields (IF, ORAC, GI).

No configuration is required in the release, but when adding your own or doing the process from scratch you will need to pair column names with known nutrient names in a "config.txt".

The full database import process is explained with `nutri db --help`

Downloading Resources
"""""""""""""""""""""

You can manually download resources on mac/Linux.

Curl for Windows requires it be put in the $PATH variable: https://curl.haxx.se/windows/

**Databases**

- Standard USDA database, 8790 foods

    `curl -L -u dasheenster:jZEZMA9hmz97e9z8dqmf  https://api.bitbucket.org/2.0/repositories/dasheenster/nutri-utils/downloads/USDAstock.txt -o USDAstock.txt`

- Branded Foods Database. **LARGE 100MB+! PC ONLY**
    
    `curl -L https://www.ars.usda.gov/ARSUserFiles/80400525/Data/BFPDB/BFPD_csv_07132018.zip -o BFPD_csv_07132018.zip`

**Supplementary USDA Extensions**

- Flavonoid, Isoflavonoids, and Proanthocyanidins
    
    `curl -L -u dasheenster:jZEZMA9hmz97e9z8dqmf  https://api.bitbucket.org/2.0/repositories/dasheenster/nutri-utils/downloads/USDA_ext_rel.zip -o USDA_ext_rel.zip`

**Fields**

**NOTE:** We are trying to start a collection of fields and make our models more general. Please upload and reach us here @ https://gitter.im/nutritracker/nutri ... (these can consist in magazine cutouts, obscure articles, or other sources of unusual nutrient data)

- Extra_fields.zip (IF, ORAC, GI, Omega-3, and anti-nutrient oxalic acid)

    `curl -L -u dasheenster:jZEZMA9hmz97e9z8dqmf  https://api.bitbucket.org/2.0/repositories/dasheenster/nutri-utils/downloads/Extra_fields.zip -o Extra_fields.zip`


Getting Set Up
==============
You need to make a user first, then import DBs.  Then think about pairing fields and custom foods.  Or just use the stock database to start making recipes and tracking simple meals.

Eventually you can track more fields and metrics on a daily basis, include more on your log, get to know your habits, and benefit from automated suggestions.

The Android app may be more intuitive for people less familiar with computers, it offers many of the same features and we are constantly working to improve that.

Usage
^^^^^

Run the `nutri` script to get a full description:

TODO: *add full commands*

**Usage:** nutri <command> 

*Commands:*

    **user**			create, edit and switch users

    **db**				import, edit and verify databases

    **field**			import, pair and manage fields

    **recipe**			create, edit and view foods and recipes

    **search**			search databases or recipes

    **add**				add foods or items to daily log

    **log**				show previous meals and summary

    **sync**			sync android device

    **contrib**			rank contribution

    **--help | -h**		show help for a given command
