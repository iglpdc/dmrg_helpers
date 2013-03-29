'''
Test for locate estimator files function.
'''
import os
from dmrg_helpers.extract.locate_estimator_files import locate_estimator_files

def test_locate_estimator_files():
    files_there = ['tests/results/one/estimators.dat', 
                   'tests/results/two/estimators.dat'] 
    files_there = map(os.path.abspath, files_there)
    files_found = locate_estimator_files('tests/results')
    print os.getcwd()
    print files_found
    print files_there
    assert files_found == files_there

