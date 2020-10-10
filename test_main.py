# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 15:19:53 2020

@author: shane

This file is part of nutra, a nutrient analysis program.
    https://github.com/nutratech/cli
    https://pypi.org/project/nutra/

nutra is an extensible nutrient analysis and composition application.
Copyright (C) 2018-2020  Shane Jaroch

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

import pytest

from ntclient.sql.funcs import usda


def test_sqlfuncs():
    result = usda.nutrients_details()
    assert len(result[1]) == 186

    result = usda.servings([9050, 9052])
    assert len(result) == 3

    result = usda.analyze_foods([23567, 23293])
    assert len(result) == 188

    result = usda.sort_foods(789)
    assert len(result) == 415
    result = usda.sort_foods(789, [100])
    assert len(result) == 1

    result = usda.sort_foods_by_kcal(789)
    assert len(result) == 246
    result = usda.sort_foods_by_kcal(789, [1100])
    assert len(result) == 127
