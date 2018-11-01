#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 23:44:06 2018

@author: shane
"""

import os
import sys
from colorama import Style, Fore, Back, init


class USER:
    def __init__(self, name, age, ht, wt, goal):
        self.dir = name
        self.name = name
        self.age = age
        self.ht = ht
        self.wt = wt
        self.goal = goal
        self.write()
        print(f'Created user "{name}"')

    def read(self, directory):
        self.dir = directory
        with open(f'{self.dir}/profile.txt', 'r') as f:
            for line in f.readlines():
                s = line.rstrip()
                if s.startswith('gender='):
                    self.gender = s.split('=')[1]
                elif s.startswith('age='):
                    self.age = int(s.split('=')[1])
                elif s.startswith('ht='):
                    self.ht = int(s.split('=')[1])
                elif s.startswith('wt='):
                    self.wt = int(s.split('=')[1])
                elif s.startswith('goal='):
                    self.goal = int(s.split('=')[1])
        self.userstr = f'{self.name} {self.ht}cm / {self.wt}kg (self.gender)'

    def write(self):
        os.makedirs(self.dir, 0o775)
        with open(f'{self.dir}/profile.txt', 'w+') as f:
            f.write(f'name={self.name}' + '\n')
            f.write(f'gender={self.gender}' + '\n')
            f.write(f'age={self.age}' + '\n')
            f.write(f'ht={self.ht}' + '\n')
            f.write(f'wt={self.wt}' + '\n')
            f.write(f'goal={self.goal}' + '\n')
            # f.write(f'activeness={self.activeness}' + '\n')


users = []


def grab_users():
    users = []
    for d in os.listdir('.nutri/users'):
        print(d)
        users.append(USER.read(d))


def listusers():
    # TODO: green asterik for current user
    for u in users:
        print(u.userstr)
    print('')


# def user_info(name):


def add(name=''):
    if name == '':
        name = input('\nPlease enter a name: ')
    for u in users:
        if u.name == name:
            exit('Error: user already exists with this name, please delete his/her directory (backup _fields and _rel first) or simply edit instead')
#    if input('U.S. Customary units? [Y/n] ').lower() == 'y':
#        usaunits = True
#    else:
#        usaunits = False
    age = int(input('Age: '))
    ht = int(input('Height: [cm] '))
    wt = int(input('Weight: [kg] '))
    print('\n  0: Sedentary\n  1: Moderate\n  2: Active\n  3: Intense\n  4: Extreme\n')
    goal = int(input('Activity Level: '))
    if goal > 4 or goal < 0:
        exit(f'Error: not a valid choice,{goal}')
    u = USER(name, age, ht, wt, goal)
    grab_users()


def main(args=sys.argv):
    os.chdir(os.path.expanduser("~"))
    os.makedirs('.nutri/users', 0o755, True)

    if args == None:
        args = sys.argv

    # No arguments passed in
    if len(args) == 0:
        print(usage)
        return
    else:
        # Pop off arg0
        if args[0].endswith('config'):
            args.pop(0)
        if len(args) == 0:
            config()
            return

    # Otherwise we have some args
    # print(args)
    for i, arg in enumerate(args):
        if arg == 'user' or arg == __file__:
            if len(args) == 1:
                listusers()
            else:
                continue
        elif arg in users:
            user_info(arg, args[i + 1:])
            break
        elif arg == '-d' or arg == '--delete':
            remove(args[i + 1:])
            break


class cmdmthds:
    """ Where we keep the `cmd()` methods && opt args """

    class remove:
        altargs = ['--delete', '-d']

        def mthd(rarg):
            remove(rarg)

    class db:
        def mthd(rarg):
            db.main(rarg)

    class help:
        altargs = ['--help', '-h']

        def mthd(rarg):
            print(usage)


def config():
    """ The default method if no args supplied. """
    try:
        pass
    except:
        pass  # ?


usage = f"""Usage: nutri config <option> [<value>]

Commands:
    process    extract headers/columns and prep data
    test       check your work before importing
    import     copy the config and data over from the lib to the resource directory
"""

if __name__ == "__main__":
    main()
