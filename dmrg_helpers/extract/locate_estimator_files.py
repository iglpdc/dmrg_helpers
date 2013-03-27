'''
File: locate_estimator_files.py
Author: Ivan Gonzalez
Description: A function to crawl a directory tree looking for files.
'''
import os
import fnmatch

def locate_estimator_files(root, pattern='estimators.dat'):
    '''Locates all the files named by the pattern in the root directory.

    You use this function to crawl a directory tree looking for estimators
    files. An estimator file is a file whose name is matched by `pattern`.

    Parameters
    ----------
    root: a string 
        The directory you want to crawl down. The name can be relative or
        absolute and must exist
    pattern: a string
        The pattern you want to match filenames with.

    Returns
    -------
    files_found a list of strings.
        The absolute paths for all the files found in a list.
    '''
    files_found = []
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            files_found.append(os.path.join(path, filename))
    return files_found
