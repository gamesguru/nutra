#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 23:44:06 2018

@author: shane
"""

import os
import sys
import getpass
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


nutridir = f'{os.path.expanduser("~")}/.nutri'


def main(args=sys.argv):
    # os.chdir(os.path.expanduser("~"))
    # os.makedirs('.nutri/users', 0o755, True)

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
        rarg = args[i:]
        # Ignore first argument, as that is filename
        if arg == __file__:
            if len(args) == 1:
                print(usage)
                continue
            else:
                continue
        # Activate method for command, e.g. `help'
        elif hasattr(cmdmthds, arg):
            getattr(cmdmthds, arg).mthd(rarg)
            break
        # Activate method for opt commands, e.g. `-h' or `--help'
        else:
            for i in inspect.getmembers(cmdmthds):
                for i2 in inspect.getmembers(i[1]):
                    if i2[0] == 'altargs' and arg in i2[1]:
                        i[1].mthd(rarg)
                        return
        # Otherwise we don't know the arg
        print(f"config: `{arg}' is not a nutri command.  See 'nutri help'.")
        break


class cmdmthds:
    """ Where we keep the `cmd()` methods && opt args """

    class new:
        altargs = ['--new', '-n']

        def mthd(rarg):
            new_profile(rarg)

    class extras:
        def mthd(rarg):
            print(extras)

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


def new_profile(rargs):
    name = getpass.getuser()
    gender = 'n'
    age = 0
    print('Warning: This will create a new profile (log and db are kept)\n')
    # Name
    inpt = input(f'Enter name (blank for {name}): ')
    if inpt != '':
        name = inpt
    # Gender
    while True:
        inpt = input(f'Gender? [m/f/n]: ')
        if inpt == 'm' or inpt == 'f' or inpt == 'n':
            gender = inpt
            break
    # Age
    while True:
        inpt = input(f'Age: ')
        try:
            inpt = int(inpt)
            if inpt > 0 and inpt < 130:
                age = inpt
                break
        except:
            pass
    # Write new profile
    os.makedirs(nutridir, 0o775, True)
    with open(f'{nutridir}/config.txt', 'w+') as f:
        f.write(f'Name:{name}\n')
        f.write(f'Gender:{gender}\n')
        f.write(f'Age:{age}\n')
    print("That's it for the basic config, you can see what more can be configured with `nutri config extras'")


usage = f"""Usage: nutri config <option> [<value>]

Options:
    new        create a new profile (log and db are kept)
    -e         configure an extra option
    extras     help for extra options (height, weight, wrist size)
"""

extras = f"""Usage: nutri config -e <option> [<value>]

Options:
    ht         height
    wt         weight
    wrist      wrist size"""

if __name__ == "__main__":
    main()
