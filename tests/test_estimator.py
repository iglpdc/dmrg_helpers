'''
Test for the database class.
'''
import os
from nose.tools import with_setup
from dmrg_helpers.extract.database import Database

def setup_function():
    pass

def teardown_function():
    os.remove('tests/db_test.sqlite3')

@with_setup(setup_function, teardown_function)
def test_members():
    db = Database('tests/db_test.sqlite3')
    db.insert_data_from_file('tests/file_one.dat')
    n_up = db.get_estimator('n_up')
    assert n_up.name == 'n_up'
    meta_keys = n_up.meta_keys
    assert 'parameter_1' in meta_keys
    assert 'parameter_2' in meta_keys
    assert len(n_up) == 1
    assert '1.0:a_string' in n_up.data.keys()

@with_setup(setup_function, teardown_function)
def test_save():
    db = Database('tests/db_test.sqlite3')
    db.insert_data_from_file('tests/file_one.dat')
    n_up = db.get_estimator('n_up')
    n_up.save_as_txt('n_up', 'tests/')
    contents = '0 1.0\n1 2.0'
    with open('tests/n_up_parameter_1_1.0_parameter_2_a_string.dat', 'r') as f:
        from_file = f.read()
    assert from_file == contents
    os.remove('tests/n_up_parameter_1_1.0_parameter_2_a_string.dat')
