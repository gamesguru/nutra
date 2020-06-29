# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:09:07 2019

@author: shane

This file is part of nutra, a nutrient analysis program.
    https://github.com/nutratech/cli
    https://pypi.org/project/nutra/

nutra is an extensible nutraent analysis and composition application.
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
"""

import getpass
import inspect
import os
import sys

import requests

from .utils.settings import NUTRA_DIR, SERVER_HOST


def request(path, params):
    # print(f'{SERVER_HOST}{path}')
    # print(params)
    return requests.get(url=f"{SERVER_HOST}{path}", params=params)


def register(args=None):
    print("Register an online account!")
    username = input("Enter a username: ")
    email = input("Enter your email: ")
    password = getpass.getpass("Enter a password: ")
    confirm_password = getpass.getpass("Confirm password: ")

    params = dict(
        username=username,
        password=password,
        confirm_password=confirm_password,
        email=email,
    )

    response = request("register", params)
    print(response.json()["message"] + ": " + response.json()["data"])


def login(args=None):
    print("Login!")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    params = dict(username=username, password=password)

    response = request("login", params)
    token = response.json()["data"]
    print("Response: " + token)

    with open(f"{NUTRA_DIR}/token", "a+") as token_file:
        token_file.write(token)
