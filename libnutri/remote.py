#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:09:07 2019

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

import os
import sys
import inspect
import getpass
import requests

LOCAL_HOST = 'http://localhost:8080'
SERVER_HOST = 'https://nutritracker-server.herokuapp.com'

nutridir = os.path.join(os.path.expanduser("~"), '.nutri')


def request(path, params):
    # print(f'{SERVER_HOST}/{path}')
    # print(params)
    return requests.get(url=f'{SERVER_HOST}/{path}', params=params)


def register(args=None):
    print('Register an online account!')
    username = input('Enter a username: ')
    email = input('Enter your email: ')
    password = getpass.getpass('Enter a password: ')
    confirm_password = getpass.getpass('Confirm password: ')

    params = dict(
        username=username,
        password=password,
        confirm_password=confirm_password,
        email=email
    )

    response = request('register', params)
    print(response.json()['message'] + ': ' + response.json()['data']['message'])


def login(args=None):
    print('Login!')
    username = input('Enter your username: ')
    password = getpass.getpass('Enter your password: ')

    params = dict(
        username=username,
        password=password
    )

    response = request('oauth', params)
    token = response.json()['data']['message']
    print('Response: ' + token)

    with open(f'{nutridir}/token', 'a+') as token_file:
        token_file.write(token)


def main(args=None):
    if args == None:
        args = sys.argv[1:]

    # No arguments passed in
    if len(args) == 0:
        print(usage)

    # Otherwise we have some args
    for i, arg in enumerate(args):
        rarg = args[i:]
        if hasattr(cmdmthds, arg):
            getattr(cmdmthds, arg).mthd(rarg[1:])
            break
        # Activate method for opt commands, e.g. `-h' or `--help'
        elif altcmd(i, arg) != None:
            altcmd(i, arg)(rarg[1:])
            break
        # Otherwise we don't know the arg
        else:
            print(f"error: unknown option `{arg}'.  See 'nutri db --help'.")
            break


def altcmd(i, arg):
    for i in inspect.getmembers(cmdmthds):
        for i2 in inspect.getmembers(i[1]):
            if i2[0] == 'altargs' and arg in i2[1]:
                return i[1].mthd
    return None


class cmdmthds:
    """ Where we keep the `cmd()` methods && opt args """
    class register:
        def mthd(rarg):
            register()

    class login:
        def mthd(rarg):
            login()

    class help:
        def mthd(rarg):
            print(usage)
        altargs = ['-h', '--help']


usage = f"""nutri: Remote connection tool

Usage: nutri remote <command>

Commands:
    list | -l  list off databases stored on your computer"""

if __name__ == "__main__":
    main()
