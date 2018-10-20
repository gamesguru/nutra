Nutritracker
------------

An extensible nutrient tracking app designed for home and office use.
CLI backend.

Downloading Resources
=====================
Can be downloaded manually, visit this link: https://bitbucket.org/dasheenster/nutri-utils/downloads/



Available resources
^^^^^^^^^^^^^^^^^^^
You can manually download resources on mac/Linux.

Otherwise curl is required for Windows: https://curl.haxx.se/windows/

**Databases**

- USDAstock.txt (Standard USDA database, 8790 foods)

    `curl -L -u dasheenster:jZEZMA9hmz97e9z8dqmf  https://api.bitbucket.org/2.0/repositories/dasheenster/nutri-utils/downloads/USDAstock.txt -o USDAstock.txt`

- BFPD_csv_07132018.zip (Branded Foods Database. **LARGE 100MB! PC ONLY**)
    
    `curl -L https://www.ars.usda.gov/ARSUserFiles/80400525/Data/BFPDB/BFPD_csv_07132018.zip -o BFPD_csv_07132018.zip`

**Supplementary Flavonoid  Database**

- USDA_ext_rel.zip (Includes flavonoid, isoflavonoids, and proanthocyanidins)
    
    `curl -L -u dasheenster:jZEZMA9hmz97e9z8dqmf  https://api.bitbucket.org/2.0/repositories/dasheenster/nutri-utils/downloads/USDA_ext_rel.zip -o USDA_ext_rel.zip`

**Fields**

- Extra_fields.zip (IF, ORAC, GI, Omega-3, and anti-nutrient oxalic acid)

    `curl -L -u dasheenster:jZEZMA9hmz97e9z8dqmf  https://api.bitbucket.org/2.0/repositories/dasheenster/nutri-utils/downloads/Extra_fields.zip -o Extra_fields.zip`

*(More to come)*

Getting Set Up
==============
You need to make a user first, then import DBs.  Then think about pairing fields and custom foods.

Eventually you can track more things on a daily basis, get to know your habits, and benefit from tips and suggestions.

Usage
^^^^^

Run the 'nutri' script to get a full description:

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
