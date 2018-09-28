#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 10:23:50 2018

@author: shane
"""

import os
import re
import sys
import shutil
from colorama import Style, Fore, Back, init

class rawtable:
    def __init__(self, file):
        print(f'{Back.RED}Processing:{Style.RESET_ALL} {file}')
        #TODO: exit if config.txt exists, or prompt to overwrite
        with open(file, 'r') as f:
            lst = f.readlines()
        self.dir = os.path.dirname(file)
        self.headers = lst[0].split('\t')
        self.pheaders = self.headers
        self.colspan = len(self.headers)
        self.rows = []
        print(f'Your data has {self.colspan} columns and {len(lst)} rows.') #, or {colspan * len(lst)} cells.')
        for n, row in enumerate(lst):
            self.rows.append(row)
            curspan = len(row.split('\t'))
            if not curspan == self.colspan:
                print(f'Error: only {curspan} elements (expect {self.colspan}) in row #{n}\n\n{row}')
                return None
        print(f'Verified {Fore.CYAN}{self.colspan * len(lst)} cells!{Style.RESET_ALL}')
        maxlength = 0
        for i, h in enumerate(self.headers):
            self.headers[i] = h.replace(' ', '_').rstrip()
            maxlength = maxlength if maxlength >= len(self.headers[i]) else len(self.headers[i])
        for i, h in enumerate(self.headers):
            self.pheaders[i] = h + ' ' * (maxlength - len(h) + 1)
        with open(f'{self.dir}/config.txt', 'w+') as f:
            for h in self.pheaders:
                f.write(h + '=\n')
        print(f'\n   A config file has been generated @ {Back.YELLOW}{Fore.BLUE}{self.dir}/config.txt{Style.RESET_ALL}\n   Please assign nutrients and run this script with the "--test" switch to check progress.  Pass in the "--import" switch when ready to import.')

class test:
    def __init__(self, directory):
        print(f'{Back.RED}Testing:{Style.RESET_ALL} {directory}\n')
        self.dir = directory
        lst = []
        with open(f'{self.dir}/config.txt', 'r') as f:
            for l in f.readlines():
                lst.append(l.rstrip())
        b = 0
        u = 0
        c = 0
        for l in lst:
            f = l.split('=')[1]
            if f == '':
                print(f'{Back.MAGENTA}{Fore.YELLOW}Blank field:{Style.RESET_ALL} {l}')
                b += 1
            elif not f in known_fields:
                print(f'{Back.RED}Unknown field:{Style.RESET_ALL} {l}')
                u += 1
            else:
                if ('(' in l and ')' in l) or ('[' in l and ']' in l):
                    ls = re.split('\(|\)|\[|\]', l.split('=')[0])
                    print(f'{Back.GREEN}{Fore.BLACK}Configure:{Style.RESET_ALL} {ls[0]}', end='')
                    print(f'{Fore.RED}({ls[1]}){Style.RESET_ALL}', end='')
                    print(f'{ls[2]}= {f}')
                else:
                    print(f'{Back.GREEN}{Fore.BLACK}Configure:{Style.RESET_ALL} {f}={l.split("=")[0]}')
                c += 1
        print(f'\nYou have {c}/{len(lst)} configured, {u} unknown, and {b} blank fields.\nIf you are satisfied with that, run this script again with the "--import" switch.')

class IMPORT:
    def __init__(self, directory):
        self.dir = directory
        print(f'{Back.RED}Importing:{Style.RESET_ALL} {directory}..', end='')
        #TODO: warn or abort if directory exists already, offer to rename?
        os.makedirs(f'../usr/{self.dir}', 0o775, True)
        shutil.copy(f'{self.dir}/config.txt', f'../usr/{self.dir}')
        shutil.copy(f'{self.dir}/data.txt', f'../usr/{self.dir}')
        print(' done!\n')

def Process():
    for d in os.listdir():
        if os.path.isdir(d) and not d.startswith('_'):
            for f in os.listdir(d):
                if f == 'data.txt':
                    rawtable(f'{d}/{f}')
def Test():
    for d in os.listdir():
        if os.path.isdir(d) and not d.startswith('_'):
            test(d)
def Import():
    for d in os.listdir():
        if os.path.isdir(d) and not d.startswith('_'):
            IMPORT(d)

def exc_main():
    if os.sep == '\\':
        init()
    print(f'\n{Fore.CYAN}Welcome to the DB import tool!{Style.RESET_ALL}\n')
    for i, arg in enumerate(sys.argv):
        if arg == __file__:
            if len(sys.argv) == 1:
                usage()
            else:
                continue
        elif arg == '--test':
            Test()
            break
        elif arg == '--import':
            Import()
            break
        elif arg == '--process':
            Process()
            break
        else:
            usage()
            break

known_fields = [
            "FoodName",
            "NDBNo",
            "OthPrimKey",
            "OthPrimKey2",
            "OthPrimKey3",
            "Serv",
            "Serv2",
            "Weight",
            "Weight2",
            "ALA",
            "EpaDha",
            "Cals",
            "CalsFat",
            "FatTot",
            "FatSat",
            "FatTrans",
            "FatMono",
            "FatPoly",
            "Cholest",
            "Na",
            "K",
            "Carbs",
            "Fiber",
            "FiberSol",
            "Sugar",
            "Protein",
            "VitA",
            "VitC",
            "Ca",
            "Fe",
            "VitD",
            "VitE",
            "VitK",
            "B1",
            "B2",
            "B3",
            "B5",
            "B6",
            "B7",
            "B9",
            "B12",
            "Mg",
            "Zn",
            "Se",
            "B",
            "I",
            "P",
            "Mn",
            "F",
            "Cu",
            "Cr",
            "Mo",
            "Choline",
            "Inositol",
            "Carnitine",
            "Lipoic acid",
            "Aminos"
            ]

def usage():
    print('usage: \n   --process\textract headers/columns and prep data\n   --test\tcheck your work before importing\n   --import\tcopy the config and data over from the lib to the resource directory')

if __name__ == "__main__":
    if os.getcwd() != os.path.dirname(os.path.realpath(__file__)):
        exit('Error: must run this script out of /lib directory, where it is located')
    exc_main()
