#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 06:38:40 2018

@author: shane
NOTICE
    This file is part of nutri, a nutrient analysis program.
        https://github.com/gamesguru/nutri
        https://pypi.org/project/nutri/

    nutri is an extensible nutrient analysis and composition application.
    Copyright (C) 2018  Shane Jaroch

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
END NOTICE
"""

from colorama import Style, Fore

# Colors
critlevel = 0.3
critcolor = Fore.RED

warnlevel = 0.7
warncolor = Fore.YELLOW

safecolor = Fore.CYAN

overlevel = 1.3
overcolor = Fore.LIGHTBLACK_EX
# End colors


def color(perc):
    if perc <= critlevel:
        return critcolor
    elif perc > critlevel and perc <= warnlevel:
        return warncolor
    elif perc > warnlevel and perc < overlevel:
        return safecolor
    else:
        return overcolor


def progbar(ing=5, rda=100, buf=25):
    perc = ing / rda
    ticks = round(perc * buf)
    ticks = ticks if ticks < buf else buf
    bar = "<"
    for i in range(ticks):
        bar += "="
    for i in range(buf - ticks):
        bar += " "
    bar += ">"
    c = color(perc)
    p = fmtperc(perc)
    fstr = f"{c}{bar} {p}{Style.RESET_ALL}"
    return fstr


def fmtperc(perc):
    p = str(perc * 100) + "%"
    for i in range(len(p), 6):
        p = f" {p}"
    return f"{color(perc)}{p}{Style.RESET_ALL}"


for i in range(0, 175, 25):
    print(progbar(i))
