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
