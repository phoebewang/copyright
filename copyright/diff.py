import os
from filecmp import dircmp

def diffdir(d1, d2):
    result = dircmp(d1, d2)
    return find_diff_files(result)

def filter_files(items, d):
    result = []
    for f in items:
        p = os.path.join(d, f)
        if os.path.isfile(p):
            result.append(p)
    return result

def find_diff_files(dcmp):
    '''Return list of differing or missing relative filenames.

    Args
    ----
    dcmp: class filecmp.dircmp
    '''
    # print('left ', dcmp.left_only)
    # print('right ', dcmp.right_only)
    # print('diff ', dcmp.diff_files)
    left_only = filter_files(dcmp.left_only, dcmp.left)
    right_only = filter_files(dcmp.right_only, dcmp.right)
    diff_files = filter_files(dcmp.diff_files, dcmp.right)
    result = left_only + right_only + diff_files

    for sub in dcmp.subdirs.values():
        result += find_diff_files(sub)

    return result

# copyright - Add or replace license boilerplate.
# Copyright (C) 2016 Remik Ziemlinski
# 
# copyright is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# copyright is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.